from qgis.core import QgsProject

layers = list(QgsProject.instance().mapLayers().values())
if not layers:
    print("No layers loaded.")
for layer in sorted(layers, key=lambda item: item.name().casefold()):
    crs = layer.crs()
    identifier = crs.authid() or crs.description() or "Unknown/custom CRS"
    if not crs.isValid():
        identifier = "Invalid or missing CRS"
    status = "valid" if layer.isValid() else "invalid"
    print(f"{layer.name()} | {identifier} | {status}")
print(f"Total registered layers: {len(layers)}")
