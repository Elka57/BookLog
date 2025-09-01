#!/usr/bin/env bash
# backend
cd backend && python manage.py runserver 0.0.0.0:8000 &

# frontend
cd frontend && npm run dev -- --host 0.0.0.0

