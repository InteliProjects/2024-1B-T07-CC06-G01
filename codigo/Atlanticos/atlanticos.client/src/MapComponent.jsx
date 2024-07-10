import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import L from 'leaflet';
import 'leaflet.markercluster';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const smallIcon = new L.Icon({
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconSize: [20, 30],
  iconAnchor: [10, 30],
  popupAnchor: [0, -30],
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  shadowSize: [30, 30],
  shadowAnchor: [10, 30],
});

const MarkerCluster = ({ markers }) => {
  const map = useMap();

  useEffect(() => {
    const markerClusterGroup = L.markerClusterGroup();

    markers.forEach((markerData) => {
      const marker = L.marker(markerData.position, { icon: smallIcon });
      marker.bindPopup(markerData.popup);
      markerClusterGroup.addLayer(marker);
    });

    map.addLayer(markerClusterGroup);

    return () => {
      map.removeLayer(markerClusterGroup);
    };
  }, [map, markers]);

  return null;
};

const MapComponent = ({ responseData }) => {
  if (!responseData || !Array.isArray(responseData) || responseData.length === 0) {
    return <div>Nenhum dado válido fornecido para exibição no mapa.</div>;
  }

  const allCoordinates = responseData.map((item) => item.coordinates);
  const allRoutes = responseData.map((item) => item.route);

  const allSortedCoordinates = allCoordinates.map((coordinates, index) => {
    const route = allRoutes[index];
    const sortedCoordinates = route.map((routeIndex) => coordinates[routeIndex]);
    return sortedCoordinates;
  });

  const markers = allSortedCoordinates.flat().map((coordinate, index) => ({
    position: coordinate,
    popup: `Ponto ${index + 1}`,
  }));

  const colors = ['blue', 'red', 'green', 'orange', 'purple'];

  return (
    <MapContainer center={[-22.8115, -43.3207]} zoom={13} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <MarkerCluster markers={markers} />
      {allSortedCoordinates.map((sortedCoordinates, groupIndex) => (
        <Polyline
          key={groupIndex}
          color={colors[groupIndex % colors.length]}
          positions={sortedCoordinates}
          weight={10}
        />
      ))}
    </MapContainer>
  );
};

export default MapComponent;
