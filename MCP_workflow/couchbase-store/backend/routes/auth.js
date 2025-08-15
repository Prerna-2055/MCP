const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');
const { getCollection } = require('../config/database');
const router = express.Router();

// Generate JWT token
const generateToken = (userId) => {
  return jwt.sign({ userId }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || '7d'
  });
};

// Register user
router.post('/register', [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 6 }),
  body('firstName').trim().isLength({ min: 1 }),
  body('lastName').trim().isLength({ min: 1 })
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { email, password, firstName, lastName } = req.body;
    const collection = getCollection();

    // Check if user already exists
    try {
      const existingUser = await collection.get(`user::${email}`);
      if (existingUser) {
        return res.status(400).json({ message: 'User already exists' });
      }
    } catch (error) {
      // User doesn't exist, continue with registration
    }

    // Hash password
    const saltRounds = 12;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // Create user document
    const userId = `user::${email}`;
    const userData = {
      type: 'user',
      email,
      password: hashedPassword,
      firstName,
      lastName,
      role: 'customer',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      isActive: true,
      profile: {
        addresses: [],
        phone: '',
        preferences: {}
      }
    };

    await collection.insert(userId, userData);

    // Generate token
    const token = generateToken(userId);

    res.status(201).json({
      message: 'User registered successfully',
      token,
      user: {
        id: userId,
        email: userData.email,
        firstName: userData.firstName,
        lastName: userData.lastName,
        role: userData.role
      }
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ message: 'Server error during registration' });
  }
});

// Login user
router.post('/login', [
  body('email').isEmail().normalizeEmail(),
  body('password').exists()
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { email, password } = req.body;
    const collection = getCollection();

    // Find user
    const userId = `user::${email}`;
    const userResult = await collection.get(userId);
    const user = userResult.content;

    if (!user || !user.isActive) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Check password
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Update last login
    await collection.upsert(userId, {
      ...user,
      lastLogin: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    });

    // Generate token
    const token = generateToken(userId);

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: userId,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ message: 'Server error during login' });
  }
});

// Get current user profile
router.get('/profile', async (req, res) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    if (!token) {
      return res.status(401).json({ message: 'No token provided' });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const collection = getCollection();
    
    const userResult = await collection.get(decoded.userId);
    const user = userResult.content;

    if (!user || !user.isActive) {
      return res.status(404).json({ message: 'User not found' });
    }

    res.json({
      user: {
        id: decoded.userId,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role,
        profile: user.profile,
        createdAt: user.createdAt
      }
    });
  } catch (error) {
    console.error('Profile fetch error:', error);
    res.status(401).json({ message: 'Invalid token' });
  }
});

module.exports = router;
