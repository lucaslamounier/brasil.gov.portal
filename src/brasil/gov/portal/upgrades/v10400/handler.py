# -*- coding:utf-8 -*-

from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.config import SHOW_DEPS
from brasil.gov.portal.setuphandlers import _instala_pacote
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

import logging

logger = logging.getLogger(PROJECTNAME)


def apply_profile(context):
    """Atualiza perfil para versao 10400"""
    profile = 'profile-brasil.gov.portal.upgrades.v10400:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 10400')


def aplica_view_noticias(context):
    """Aplica visao sumaria para pasta Noticias"""
    portal = api.portal.get()
    noticias = portal['noticias']
    if (noticias):
        noticias.setLayout('folder_summary_view')
        noticias.reindexObject()
        logger.info(u'Visão sumária aplicada na pasta Notícias')