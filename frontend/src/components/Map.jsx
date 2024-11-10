import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function MapComponent() {
  const [geojsonData, setGeojsonData] = useState(null);
  const [selectedTracts, setSelectedTracts] = useState(new Set()); // Track selected tracts by CTNAME
  const [isLocked, setIsLocked] = useState(false); // Lock selection after submission

  useEffect(() => {
    fetch("/population_map.geojson")
      .then((response) => response.json())
      .then((data) => setGeojsonData(data))
      .catch((error) => console.error("Error loading GeoJSON:", error));
  }, []);

  // Toggle selection of a tract by its CTNAME
  const handleTractClick = (tractName) => {
    if (!isLocked) {
      setSelectedTracts((prevSelected) => {
        const newSelected = new Set(prevSelected);
        if (newSelected.has(tractName)) {
          newSelected.delete(tractName); // Deselect if already selected
        } else {
          newSelected.add(tractName); // Select if not already selected
        }
        return newSelected;
      });
    }
  };

  // Lock selection to prevent further changes
  const handleSubmit = () => {
    setIsLocked(true);
    console.log(selectedTracts);
    for (let tract_id of selectedTracts) {
      fetch(`http://127.0.0.1:8000/api/find-stops/?danger_tract_id=${tract_id}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json(); // Parse the JSON response
        })
        .then((data) => {
          console.log(data); // Log the parsed data
        })
        .catch((error) => {
          console.error("Fetch error:", error);
        });
    }
  };

  return (
    <div>
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
            style={(feature) => ({
              color: selectedTracts.has(feature.properties.CTUID)
                ? "red"
                : "#000000", // Toggle color based on selection
              fillColor: selectedTracts.has(feature.properties.CTUID)
                ? "red"
                : "#00FF00", // Green if not selected
              weight: 2,
              fillOpacity: 0.5,
            })}
            onEachFeature={(feature, layer) => {
              layer.on("click", () =>
                handleTractClick(feature.properties.CTUID)
              ); // Handle click to toggle selection
              if (feature.properties && feature.properties.CTUID) {
                layer.bindPopup(`Tract: ${feature.properties.CTUID}`);
              }
            }}
          />
        )}
      </MapContainer>

      <button onClick={handleSubmit} style={{ marginTop: "10px" }}>
        Submit Selection
      </button>
    </div>
  );
}

export default MapComponent;
