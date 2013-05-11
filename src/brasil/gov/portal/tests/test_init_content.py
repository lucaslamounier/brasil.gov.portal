# -*- coding: utf-8 -*-

from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

import unittest


class InitContentTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        profile = 'profile-brasil.gov.portal:initcontent'
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        wf = self.portal.portal_workflow
        wf.setDefaultChain('simple_publication_workflow')
        types = ('Document', 'Folder', 'Link', 'Topic', 'News Item')
        wf.setChainForPortalTypes(types, '(Default)')
        self.st = self.portal.portal_setup
        self.st.runAllImportStepsFromProfile(profile)
        self.wt = self.portal.portal_workflow

    def test_assuntos_available(self):
        self.assertTrue('assuntos' in self.portal.objectIds(),
                        u'Pasta Assuntos não disponível')
        pasta = self.portal['assuntos']
        self.assertEquals(u'Assuntos', pasta.title,
                          u'Título não aplicado')
        self.assertEquals(self.wt.getInfoFor(pasta, 'review_state'),
                          'published')

    def test_imagens_available(self):
        self.assertTrue('imagens' in self.portal.objectIds(),
                        u'Pasta Imagens não disponível')
        pasta = self.portal['imagens']
        self.assertEquals(u'Imagens', pasta.title,
                          u'Título não aplicado')
        self.assertEquals(self.wt.getInfoFor(pasta, 'review_state'),
                          'published')

    def test_imagens_constrains(self):
        pasta = self.portal['imagens']
        behavior = ISelectableConstrainTypes(pasta)
        types = ['Image']
        self.assertEqual(types, behavior.getImmediatelyAddableTypes())

    def test_servicos_available(self):
        self.assertTrue('servicos' in self.portal.objectIds(),
                        u'Pasta Servicos não disponível')
        pasta = self.portal['servicos']
        self.assertEquals(u'Serviços', pasta.title,
                          u'Título não aplicado')
        self.assertEquals(self.wt.getInfoFor(pasta, 'review_state'),
                          'published')

    def test_servicos_constrains(self):
        pasta = self.portal['servicos']
        behavior = ISelectableConstrainTypes(pasta)
        types = ['Link']
        self.assertEqual(types, behavior.getImmediatelyAddableTypes())

    def test_sobre_available(self):
        self.assertTrue('sobre' in self.portal.objectIds(),
                        u'Pasta Sobre não disponível')
        pasta = self.portal['sobre']
        self.assertEquals(u'Sobre', pasta.title,
                          u'Título não aplicado')
        self.assertEquals(self.wt.getInfoFor(pasta, 'review_state'),
                          'published')

    def test_default_portlets(self):
        # Os portlets estao configurados corretamente?
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        self.assertEquals(len(mapping.keys()), 2)
        self.assertTrue('assuntos' in mapping.keys())
        self.assertTrue('sobre' in mapping.keys())

    def test_portlet_assuntos(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # Assuntos
        self.assertEquals(mapping['assuntos'].root, u'/assuntos')
        self.assertEquals(mapping['assuntos'].name, u'Assuntos')
        self.assertEquals(mapping['assuntos'].currentFolderOnly, False)

    def test_portlet_sobre(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # Sobre
        self.assertEquals(mapping['sobre'].root, u'/sobre')
        self.assertEquals(mapping['sobre'].name, u'Sobre')
        self.assertEquals(mapping['sobre'].currentFolderOnly, False)