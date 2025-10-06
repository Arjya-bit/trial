from elasticsearch import Elasticsearch
from ..core.config import settings

es = Elasticsearch(settings.elastic_url)
