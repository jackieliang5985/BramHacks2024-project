import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function MapComponent() {
  const [geojsonData, setGeojsonData] = useState(null);

  useEffect(() => {
    fetch("/population_map.geojson")
      .then((response) => response.json())
      .then((data) => setGeojsonData(data))
      .catch((error) => console.error("Error loading GeoJSON:", error));
  }, []);

  return (
    <MapContainer
      center={[43.6849, -79.7595]}
      zoom={11}
      style={{ height: "600px", width: "600px" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {geojsonData && (
        <GeoJSON
          data={geojsonData}
          style={() => ({
            color: "#FF0000",
            fillColor: "#FF0000",
            weight: 2,
            fillOpacity: 0.5,
          })}
          onEachFeature={(feature, layer) => {
            if (feature.properties && feature.properties.name) {
              layer.bindPopup(feature.properties.name);
            }
          }}
        />
      )}
    </MapContainer>
  );
}

export default MapComponent;
