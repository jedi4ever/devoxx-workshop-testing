import logging
logger = logging.getLogger(__name__)

class BaseSettings(object):

    metadata_fields = {}

    def update(self, settings, state):

        # check for metadata fields in metadata
        metadata = state.metadata
        logger.debug("metadata : %s", metadata)
        for key, value in self.metadata_fields.items():
            logger.debug("checking %s : %s", key, getattr(self, key ))
            if key in metadata:
                meta_value = metadata[key]
                if (meta_value is not None):
                    logger.debug("setting %s : %s", key,meta_value)
                    setattr(self, key, meta_value)
            else:
                logger.debug("key %s not in metadata", key)

        # next have settings override the metadata fields
        for key, value in settings.items():
            if (value is not None):
                logger.debug("setting %s : %s", key, value)
                setattr(self, key, value)
