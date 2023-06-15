"""Inject the current asset type into the context."""
import pyblish.api


class CollectAssetType(pyblish.api.ContextPlugin):
    """Inject the current asset type into context."""

    order = pyblish.api.CollectorOrder
    label = f"Asset Type"
    version = (0, 1, 0)
    hosts = ['blender']

    def process(self, context):
        """Inject the asset type."""
        from pathlib import Path
        current_file = Path(context.data['currentFile'])
        context.data['isModularAsset'] = is_modular = "sets" in [
            _.stem for _ in current_file.parents]
        if is_modular:
            # e.g. sets/entire-library/footwear/sneakers/sneakers-07/working-files -> get 'footwear'
            asset_type = current_file.parent.parent.parent.parent.stem
        else:
            asset_type = current_file.stem.split("-")[0]
        if not asset_type:
            asset_type = "unknown"
        context.data['assetType'] = asset_type
        self.log.info(f"Asset Type: {asset_type}")
