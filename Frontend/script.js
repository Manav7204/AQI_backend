document.addEventListener("DOMContentLoaded", () => {
    const predictBtn = document.getElementById("predictBtn");

    predictBtn.addEventListener("click", () => {
        const city = document.getElementById("cityInput").value.trim();

        if (city !== "Mumbai") {
            alert("Only Mumbai is supported for now.");
            return;
        }

        // 🔗 Replace this with your running FastAPI server URL if different
        fetch("https://aqi-backend-itir.onrender.com/predict")
            .then(response => {
                if (!response.ok) {
                    throw new Error("FastAPI server did not respond correctly.");
                }
                return response.json();
            })
            .then(data => {
                // ✅ Update predicted AQI and other info
                document.getElementById("predictedAqi").textContent = data.predicted_aqi;
                document.getElementById("currentAqi").textContent = data.current_aqi;
                document.getElementById("dateInfo").textContent = `${data.date} (${data.day})`;

                // ✅ Populate features list dynamically
                const featureList = document.getElementById("featureData");
                featureList.innerHTML = "";

                Object.entries(data.features).forEach(([key, value]) => {
                    const li = document.createElement("li");
                    li.textContent = `${key}: ${value}`;
                    featureList.appendChild(li);
                });
            })
            .catch(err => {
                alert("Error fetching AQI data. Make sure FastAPI is running.");
                console.error("Fetch error:", err);
            });
    });
});
