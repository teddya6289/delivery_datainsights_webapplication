# Secure Authentication & Role-Based  Analytics Deliverable Platform

## Overview

This project is a Flask-based web application that combines **enterprise-grade authentication security,Activity monitoring and Contol** with **User registeration with role select with role-based analytical delivery**.

It was designed to address two critical concerns in modern business systems:

1. Secure user authentication,monitoring,control and recovery workflows
2. Controlled access to actionable business KPIs based on user roles

---

## Core Features

### Authentication & Security

- Stateless, time-bound token verification (password reset & email verification)
- One-time password reset enforcement
- DOB verification with masked hints
- Rate limiting per user and per IP
- Automatic account lockout after repeated failures
- Centralized session inactivity timeout
- Correct HTTP error handling with custom error pages
- No reliance on `current_user` for token-based flows

---

### Role-Based KPI Analytics

A protected analytics route dynamically adjusts content based on user role.

#### Procurement Manager
- Monthly total number of units sold
- Best-selling products
- Worst-selling products
- Inventory-focused insights

#### Sales Manager
- Monthly total sales revenue
- Product-level revenue breakdown
- Best vs worst sellers for the month

#### Visualizations
- Graphs displaying:
  - Top-performing products
  - Lowest-performing products
- Monthly aggregation logic handled server-side
- Strict role-based access enforcement

---

## Tech Stack

| Layer | Technology |
|-----|-----------|
|Database|SQLALCHEMY BIND:Oracle and SQL Server|
Backend | Flask (Application Factory Pattern) |
Authentication | Flask-Login |
Rate Limiting | Flask-Limiter |
Email | Flask-Mail |
ORM | SQLAlchemy |
Templating | Jinja2 |
Security Tokens | itsdangerous |
Time Handling | datetime, timedelta |
Visualization | Server-side aggregation + chart rendering |

---

## Architecture Highlights

- Blueprint-based routing
- Centralized `before_request` session enforcement
- Token-based flows isolated from session logic
- Role-based access control at the route level
- Clean separation of business logic, security, and presentation

---

## Error Handling

- All errors raised via `abort(code, description=...)`
- Global HTTP exception handler
- Custom `error.html` template
- Correct HTTP status codes preserved (401, 403, 404, 429)

---

## Security Principles Applied

- Least privilege access
- Stateless verification
- Defense against brute-force and abuse
- Explicit timeout handling using `timedelta`
- No implicit trust of client or session state

---

## Future Enhancements

- Export KPI reports (PDF / CSV)
- Admin dashboard for role management
- Async email delivery
- Audit logging for security events
- API version of analytics endpoints

---
Developed with a focus on **security-first backend design** and **business-driven analytics**.

Feel free to explore, fork, or reach out with questions.
