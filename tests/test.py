# -*- coding: utf-8 -*-
"""Dash Tutorial Testing.

See:

"""
#     ///// //// /// // //    AAAAAAAAAA  MMMM     MMMM  GGGGGGGGGG
#    ///// //// /// // //    AAAA   AAAA  MM MM   MM MM  GG
#   ///// //// /// // //    AAAA    AAAA  MM  MM MM  MM  GG  GGGGGG
#  ///// //// /// // //    AAAAAAAAAAAAA  MM   MMM   MM  GG      GG
# ///// //// /// // //    AAAA      AAAA  MM         MM  GGGGGGGGGG
#                        ANALYTICS

"""
Created on 13.07.2021

@author: Karge, L.
"""


# test utils
import pytest, os
from app import app, amg_you_rock
# system imports


class TestApp(object):
    
    @classmethod
    def setup_class(cls):
        pass  

    def test_app(self):
        app

    def test_amg_you_rock(self):
        assert amg_you_rock() == '''AMG you rock!'''
        