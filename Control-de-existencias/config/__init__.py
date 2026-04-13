"""Configuración de la aplicación - punto de entrada centralizado."""

from config.settings import config, Config, DevelopmentConfig, TestingConfig, ProductionConfig

__all__ = ['config', 'Config', 'DevelopmentConfig', 'TestingConfig', 'ProductionConfig']

