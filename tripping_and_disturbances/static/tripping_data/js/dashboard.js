let originalData = []; // Store original fetched data

document.addEventListener("DOMContentLoaded", function () {
    fetchIncidentData(); // Fetch API data and then initialize everything
});

// Step 1: Fetch data from API
async function fetchIncidentData() {
    try {
        const response = await fetch("/api/incidents/");
        const data = await response.json();
        console.log("Fetched incident data:", data);

        originalData = data;

        populateTable(data);
        populateDropdowns(data);
        renderAllCharts(data);
        setupFilterListeners(); // <-- Important: attach filter event handlers
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Step 2: Setup Filter Event Listeners
function setupFilterListeners() {
    document.querySelectorAll('.filters select').forEach(select => {
        select.addEventListener('change', () => {
            const filtered = getFilteredData();
            populateTable(filtered);
            renderAllCharts(filtered);
        });
    });
}

// Step 3: Filter the Data Based on Dropdowns
function getFilteredData() {
    const fy = document.querySelector(".filters select:nth-child(1)").value;
    const head = document.querySelector(".filters select:nth-child(2)").value;
    const month = document.querySelector(".filters select:nth-child(3)").value;

    return originalData.filter(item => {
        const matchFY = fy === "Financial Year" || item.financial_year === fy;
        const matchHead = head === "Site Head" || item.site_head === head;
        const matchMonth = month === "Month" || item.month === month;
        return matchFY && matchHead && matchMonth;
    });
}

// Step 4: Render All Charts
function renderAllCharts(data) {
    initializeChart(data);
    initializeSPVChart(data);
    initializeChart3(data);
}

// Step 5: Chart 1 - Monthly Tripping
function initializeChart(data) {
    const container = document.getElementById('chart1');
    if (!container) return;

    const monthlyData = Array(12).fill(0);
    data.forEach(item => {
        const date = new Date(item.incident_date);
        const monthIndex = date.getMonth();
        monthlyData[monthIndex]++;
    });

    const options = {
        series: [{ name: "Incidents", data: monthlyData }],
        chart: {
            height: 350,
            type: 'line',
            zoom: { enabled: false },
            toolbar: { show: false }
        },
        dataLabels: { enabled: false },
        stroke: { curve: 'straight' },
        title: { text: 'Monthly Tripping', align: 'left' },
        grid: {
            row: { colors: ['#f3f3f3', 'transparent'], opacity: 0.5 }
        },
        xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        }
    };

    container.innerHTML = '';
    const chart = new ApexCharts(container, options);
    chart.render();
}

// Step 6: Chart 2 - SPV Wise
function initializeSPVChart(data) {
    const container = document.getElementById('chart2');
    if (!container) return;

    const spvMap = {};
    data.forEach(item => {
        const spv = item.spv;
        const monthIndex = new Date(item.incident_date).getMonth();
        if (!spvMap[spv]) spvMap[spv] = Array(12).fill(0);
        spvMap[spv][monthIndex]++;
    });

    const series = Object.entries(spvMap).map(([spv, counts]) => ({
        name: spv,
        data: counts
    }));

    const options = {
        series,
        chart: {
            height: 350,
            type: 'line',
            zoom: { enabled: false },
            toolbar: { show: false }
        },
        dataLabels: { enabled: false },
        stroke: { curve: 'smooth', width: 3 },
        title: { text: 'SPV-wise Disturbance Trends', align: 'left' },
        legend: { position: 'top', horizontalAlign: 'right' },
        grid: {
            row: { colors: ['#f3f3f3', 'transparent'], opacity: 0.5 }
        },
        xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        }
    };

    container.innerHTML = '';
    new ApexCharts(container, options).render();
}

// Step 7: Chart 3 - Disturbance Type
function initializeChart3(data) {
    const container = document.getElementById('chart3');
    if (!container) return;

    const disturbanceCount = Array(12).fill(0);
    data.forEach(item => {
        if (item.disturbance_type) {
            const monthIndex = new Date(item.incident_date).getMonth();
            disturbanceCount[monthIndex]++;
        }
    });

    const options = {
        series: [{ name: "Disturbance Type", data: disturbanceCount }],
        chart: {
            height: 350,
            type: 'line',
            zoom: { enabled: false },
            toolbar: { show: false }
        },
        dataLabels: { enabled: false },
        stroke: { curve: 'straight' },
        title: { text: 'Disturbance Trends by Month', align: 'left' },
        grid: {
            row: { colors: ['#f3f3f3', 'transparent'], opacity: 0.5 }
        },
        xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        }
    };

    container.innerHTML = '';
    new ApexCharts(container, options).render();
}

// Step 8: Table Rows
function populateTable(data) {
    const tbody = document.querySelector(".report tbody");
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = `
          <tr>
            <td>${item.spv}</td>
            <td>${item.line_name}</td>
            <td>${item.criticality}</td>
            <td>${item.incident_date}</td>
            <td>${item.disturbance_type}</td>
            <td>${item.disturbance_category}</td>
            <td>${item.outage_hrs}</td>
            <td>${item.risk_factor}</td>
          </tr>
        `;
        tbody.innerHTML += row;
    });
}

// Step 9: Dropdowns
function populateDropdowns(data) {
    const fySelect = document.querySelector(".filters select:nth-child(1)");
    const headSelect = document.querySelector(".filters select:nth-child(2)");
    const monthSelect = document.querySelector(".filters select:nth-child(3)");

    const fySet = new Set();
    const headSet = new Set();
    const monthSet = new Set();

    data.forEach(item => {
        if (item.financial_year) fySet.add(item.financial_year);
        if (item.site_head) headSet.add(item.site_head);
        if (item.month) monthSet.add(item.month);
    });

    fySelect.innerHTML = '<option>Financial Year</option>' + [...fySet].map(v => `<option>${v}</option>`).join('');
    headSelect.innerHTML = '<option>Site Head</option>' + [...headSet].map(v => `<option>${v}</option>`).join('');
    monthSelect.innerHTML = '<option>Month</option>' + [...monthSet].map(v => `<option>${v}</option>`).join('');
}


