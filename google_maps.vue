<template>
  <div>
    <div id="map" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<script>
export default {
  mounted() {
    // Load the Google Maps API
    this.loadGoogleMapsAPI().then(() => {
      // Initialize the map
      this.initMap();
    });
  },
  methods: {
    loadGoogleMapsAPI() {
      return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyDORgwx60MCTXytGWkpkucUdVuzUsHfaU0&callback=initGoogleMaps";
        script.async = true;
        script.defer = true;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    },
    initMap() {
      // Create a new map instance
      const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 37.7749, lng: -122.4194 }, // Set the initial center coordinates
        zoom: 12, // Set the initial zoom level
      });
      
      // Add any additional map configuration or markers as needed
      
      // Example: Add a marker to the map
      new google.maps.Marker({
        position: { lat: 37.7749, lng: -122.4194 }, // Set the marker position
        map: map, // Specify the map instance
        title: "Marker Title", // Set the marker title (optional)
      });
    },
  },
};
</script>

<style scoped>
#map {
  height: 100%;
}
</style>
