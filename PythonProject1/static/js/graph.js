// Flask API'den veri çek
fetch('/api/graph-data')
    .then(response => response.json())
    .then(data => {
        const width = 1000;
        const height = 1000;
        const radius = 800; // Dağılım yarıçapı

        const svgContainer = d3.select("#author-graph")
                               .append("svg")
                               .attr("width", "100%")
                               .attr("height", "1000px")
                               .attr("viewBox", `0 0 ${width} ${height}`);

        // Zoom ve pan davranışı
        const zoom = d3.zoom()
            .scaleExtent([0.2, 4])
            .on("zoom", (event) => {
                graphGroup.attr("transform", event.transform);
            });

        const graphGroup = svgContainer.append("g");
        svgContainer.call(zoom);

        // Dairesel alan içinde tutmak için özel kuvvet
        function forceCluster() {
            const strength = 0.15;
            const centerX = width / 2;
            const centerY = height / 2;

            function force(alpha) {
                for (let i = 0, n = data.nodes.length, node; i < n; ++i) {
                    node = data.nodes[i];
                    const dx = node.x - centerX;
                    const dy = node.y - centerY;
                    const r = Math.sqrt(dx * dx + dy * dy);
                    if (r > radius) {
                        const k = (radius - r) * strength * alpha;
                        node.x = dx * k / r + node.x;
                        node.y = dy * k / r + node.y;
                    }
                }
            }

            force.initialize = function(_) {
                data.nodes = _;
            }

            return force;
        }

        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links)
                .id(d => d.id)
                .distance(100))
            .force("charge", d3.forceManyBody()
                .strength(-200))
            .force("cluster", forceCluster())
            .force("collide", d3.forceCollide().radius(30))
            .force("center", d3.forceCenter(width / 2, height / 2).strength(0.1));

        // Bağlantılar (Linkler)
        const link = graphGroup.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(data.links)
            .enter()
            .append("line")
            .attr("class", "link")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
            .attr("stroke-width", 1.5);


// Makale ortalamasını hesapla
const averagePapers = data.nodes.reduce((sum, node) => sum + node.papers, 0) / data.nodes.length;
const threshold = averagePapers * 0.2;

// Düğüm boyut ve renk skalasını belirle
const scaleRadius = d3.scaleLinear()
    .domain([0, averagePapers + threshold])
    .range([13, 21]); // Yüzde 20 altında küçük, üstünde büyük

  // BLUEVIOLET RENK SKALASI (Ton farkını artırdık)
        const scaleColor = d3.scaleLinear()
            .domain([0, averagePapers + threshold])
            .range(["#9b4dff", "blueviolet","#4b0082"]); // Daha belirgin bir renk geçişi (Açık BlueViolet'tan koyu Purple'a)

        // Düğümler (Nodes)
        const node = graphGroup.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(data.nodes)
            .enter()
            .append("circle")
            .attr("r", d => scaleRadius(d.papers)) // Makale sayısına göre boyut
            .attr("fill", d => scaleColor(d.papers)) // Makale sayısına göre renk
            .on("click", (event, d) => {
                // Ekranın tam ortasında konumlandır
                const panelWidth = 300; // Panelin genişliği (örnek olarak)
                const panelHeight = 200; // Panelin yüksekliği (örnek olarak)
                const screenWidth = window.innerWidth;
                const screenHeight = window.innerHeight;

                // Bilgi panelini ekranın ortasında yerleştir
                const left = (screenWidth - panelWidth) / 2 - 640;
                const top = (screenHeight - panelHeight) / 2 - 307;

                // Tıklanan düğümün bilgilerini göster
                const infoPanel = d3.select("#info-panel");
                infoPanel.html(`
                    <h3>${d.name}</h3>
                    <p><strong>ID:</strong> ${d.orcid}</p> 
                    <p><strong>Makaleler:</strong></p>
                    <ul>
                        ${(d.details.papers || []).map((article, index) => `<li>${index + 1} - ${article}</li>`).join('')}
                    </ul>
                    <p><strong>Bağlantılar:</strong></p>
                    <ul>
                        ${Object.entries(d.details.connections || {})
                            .map(([key, value]) => `<li>${key}: ${value}</li>`).join('')}
                    </ul>`);
                infoPanel.style("display", "block")
                         .style("left", `${left}px`)
                         .style("top", `${top}px`);
                 // Arka plan rengini kaldırmak için:
                infoPanel.style("background-color", "transparent");
            })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        // Etiketler (Labels)
        const labels = graphGroup.append("g")
            .selectAll("text")
            .data(data.nodes)
            .enter()
            .append("text")
            .text(d => d.name)
            .attr("font-size", "12px")
            .attr("fill", "gray")
            .attr("font-weight", "bold");
        // Simülasyonu çalıştır
        simulation.on("tick", () => {
            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node.attr("cx", d => d.x)
                .attr("cy", d => d.y);

            labels.attr("x", d => d.x + 12)
                  .attr("y", d => d.y + 3);
        });

        // Zoom in / Zoom out butonları
        d3.select("#zoom-in").on("click", () => {
            svgContainer.transition().call(zoom.scaleBy, 1.2);
        });

        d3.select("#zoom-out").on("click", () => {
            svgContainer.transition().call(zoom.scaleBy, 0.8);
        });

        // Sürükleme fonksiyonları
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

        // Sayfa dışında bir yere tıklayınca bilgi panelini gizle
        document.addEventListener("click", (event) => {
            const infoPanel = document.getElementById("info-panel");
            const withinBoundaries = event.target.closest("#info-panel") || event.target.closest("circle");
            if (!withinBoundaries) {
                infoPanel.style.display = "none";
            }
        });
    })
    .catch(error => console.error("Veri çekme hatası:", error));

