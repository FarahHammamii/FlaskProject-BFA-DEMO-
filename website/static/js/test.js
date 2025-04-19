document.addEventListener("DOMContentLoaded", function () {
    // Simulate a delay for loading the database
    setTimeout(function () {
      document.getElementById("loading-screen").style.display = "none";
      document.getElementById("main-content").style.display = "block";
    }, 3000); // 3 seconds delay, adjust as needed
    initializeDashboard();
  });
  
  function showAdmins() {
    document.getElementById("admin-section").style.display = "block";
    document.getElementById("formateur-section").style.display = "none";
  }
  
  function showFormateurs() {
    document.getElementById("admin-section").style.display = "none";
    document.getElementById("formateur-section").style.display = "block";
  }
  
  // Example data, replace with actual data fetching and rendering logic
  const adminData = [
    {
      id: 1,
      email: "admin1@example.com",
      firstName: "John",
      lastName: "Doe",
      image: "https://via.placeholder.com/50",
    },
    {
      id: 2,
      email: "admin2@example.com",
      firstName: "Jane",
      lastName: "Smith",
      image: "https://via.placeholder.com/50",
    },
  ];
  
  const formateurData = {
    total: 20,
    byMonth: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    countries: ["France", "Germany", "USA"],
    domaines: { Math: 20, Science: 30, History: 50 },
  };
  
  
  function renderActivityChart() {
    const ctx = document.getElementById("activityChart").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
        ],
        datasets: [
          {
            label: "Nb d'activité",
            data: [12, 19, 3, 5, 2, 3, 10, 15, 20, 25, 22, 30],
            backgroundColor: "#fff",
            borderColor: "#1c3f98",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false, // Ensure the chart does not maintain aspect ratio
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
  
  function renderTopAdmins() {
    const topAdminsList = document.getElementById("top-admins");
    topAdminsList.innerHTML = "";
  
    // Sort adminData to get the top 3 admins based on activities (descending order)
    const sortedAdmins = adminData.slice().sort((a, b) => b.activities - a.activities);
    const top3Admins = sortedAdmins.slice(0, 3);
  
    top3Admins.forEach((admin, index) => {
      const barContainer = document.createElement("div");
      barContainer.classList.add("top-admin-bar");
  
      // Create image element
      const adminImage = document.createElement("img");
      adminImage.src = admin.image;
      adminImage.alt = `Admin Image - ${admin.firstName} ${admin.lastName}`;
      adminImage.classList.add("admin-image");
  
      // Create bar element
      const bar = document.createElement("div");
      bar.classList.add("bar");
  
      // Determine the height of the bar based on activities
      const maxHeight = sortedAdmins[0].activities; // Activities of the top admin
      const barHeight = (admin.activities / maxHeight) * 100;
      bar.style.height = `${barHeight}%`;
  
      // Create label element
      const label = document.createElement("div");
      label.classList.add("label");
      label.textContent = `${admin.firstName} ${admin.lastName}`;
  
      // Append elements to the barContainer
      bar.appendChild(label);
      barContainer.appendChild(bar);
      barContainer.appendChild(adminImage);
      topAdminsList.appendChild(barContainer);
    });
  }
  
  function renderPrivilegesChart() {
    const ctx = document.getElementById("privilegesChart").getContext("2d");
    new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["Ajouter", "Supprimer", "Modifier"],
        datasets: [
          {
            label: "Privilèges",
            data: [10, 5, 15],
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
    });
  }
  
  function renderFormateursData() {
    const totalFormateurs = document.getElementById("total-formateurs");
    totalFormateurs.textContent = formateurData.total;
    const ctx = document.getElementById("formateursChart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
        ],
        datasets: [
          {
            label: "Nb de formateurs ajoutés par mois",
            data: formateurData.byMonth,
            borderColor: "#1c3f98",
            borderWidth: 1,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false, // Ensure the chart does not maintain aspect ratio
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  
    const domainesList = document.getElementById("formateurs-domaines");
    domainesList.innerHTML = "";
    for (const [domain, percentage] of Object.entries(formateurData.domaines)) {
      const listItem = document.createElement("li");
      listItem.textContent = `${domain}: ${percentage}%`;
      domainesList.appendChild(listItem);
    }
  
  
  }
  

  
  // Initial rendering
  renderAdminTable();
  renderActivityChart();
  renderTopAdmins();
  renderPrivilegesChart();
  renderFormateursData();
  