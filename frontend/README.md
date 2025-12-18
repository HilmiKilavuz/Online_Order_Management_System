# Web UI for Auth Service

## 🎨 Beautiful Web Interface

A modern, responsive web UI to interact with your deployed Auth Service on AWS!

---

## 🚀 Quick Start

### **Step 1: Update API URL**

1. Open `app.js`
2. Find line 2:
   ```javascript
   const API_URL = 'http://YOUR-ALB-DNS-HERE.eu-north-1.elb.amazonaws.com';
   ```
3. Replace with YOUR load balancer DNS:
   ```javascript
   const API_URL = 'http://order-system-alb-XXXXX.eu-north-1.elb.amazonaws.com';
   ```

### **Step 2: Open in Browser**

Simply double-click `index.html` or open it in your browser!

---

## ✨ Features

### **Landing Page**
- Beautiful gradient background with animated orbs
- Real-time API status indicator
- Stats showing your AWS deployment
- Login and registration forms

### **Dashboard**
- User profile display
- JWT token viewer with copy button
- Service status indicators
- AWS architecture diagram
- Smooth animations and transitions

### **Design**
- Glassmorphism effects
- Gradient backgrounds
- Smooth animations
- Fully responsive
- Toast notifications
- Modern typography (Inter font)

---

## 🎯 How to Use

1. **Register**: Create a new account
2. **Login**: Sign in with your credentials
3. **View Dashboard**: See your profile and JWT token
4. **Copy Token**: Use the token for API calls
5. **Logout**: Clear session and return to login

---

## 🔧 Customization

### **Colors**

Edit CSS variables in `styles.css`:

```css
:root {
    --primary: #667eea;
    --secondary: #764ba2;
    --success: #10b981;
    /* ... */
}
```

### **API Endpoints**

All endpoints are in `app.js`:
- `/health` - Health check
- `/register` - User registration
- `/login` - User login
- `/me` - Get user profile (protected)

---

## 📱 Responsive Design

Works perfectly on:
- Desktop (1920px+)
- Laptop (1024px+)
- Tablet (768px+)
- Mobile (320px+)

---

## 🎊 What You're Seeing

When you use this UI, you're:
- ✅ Making real API calls to AWS
- ✅ Authenticating with JWT tokens
- ✅ Storing data in your database
- ✅ Using your deployed microservice!

---

**Enjoy your beautiful UI!** 🚀
