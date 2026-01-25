"""Основной модуль приложения."""

from fastapi import FastAPI

from app.core.config import AppSettings, get_app_settings

app_settings: AppSettings = get_app_settings()

app: FastAPI = FastAPI(title=app_settings.APP_NAME, version=app_settings.APP_VERSION)
