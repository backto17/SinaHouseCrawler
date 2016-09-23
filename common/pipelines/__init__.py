# coding: utf-8
'''
@date: 2016-09-08
@author: alex.lin
'''
from common.pipelines.relationaldb import AsyncSqlPipelineBase
from common.pipelines.removeduplicate import RemoveDuplicatePipeline

__all__ = ['AsyncSqlPipelineBase', 'RemoveDuplicatePipeline']