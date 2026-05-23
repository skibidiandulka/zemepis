// Globe.js - 3D zeměkoule s Three.js

class Globe {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.globe = null;
        this.controls = null;
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        this.countries = [];
        this.selectedMarker = null;

        this.init();
        this.animate();
        this.addEventListeners();
    }

    init() {
        // Scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0a0a);

        // Camera
        this.camera = new THREE.PerspectiveCamera(
            60,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.z = 3;

        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.container.appendChild(this.renderer.domElement);

        // Orbit Controls pro otáčení myší
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.enableZoom = true;
        this.controls.minDistance = 2;
        this.controls.maxDistance = 8;
        this.controls.autoRotate = true;
        this.controls.autoRotateSpeed = 0.5;

        // Světla
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 3, 5);
        this.scene.add(directionalLight);

        // Vytvoření zeměkoule
        this.createGlobe();

        // Resize handler
        window.addEventListener('resize', () => this.onWindowResize());
    }

    createGlobe() {
        // Sféra jako zeměkoule
        const geometry = new THREE.SphereGeometry(1, 64, 64);

        // Načtení lokální textury zeměkoule
        const textureLoader = new THREE.TextureLoader();

        // Blank political map - jen obrysy kontinentů
        const earthTexture = textureLoader.load('textures/earth.png');

        // Materiál s texturou
        const material = new THREE.MeshPhongMaterial({
            map: earthTexture,
            shininess: 5,
            specular: 0x222222
        });

        this.globe = new THREE.Mesh(geometry, material);
        this.scene.add(this.globe);

        // Načtení průměrných pozic zemí
        this.loadAveragedCountries();
    }

    loadAveragedCountries() {
        fetch('data/countries_averaged.json')
            .then(response => response.json())
            .then(data => {
                console.log(`Načteno ${data.length} zemí z průměrných dat`);
                this.createCountryMarkersFromLatLon(data);
            })
            .catch(error => {
                console.error('Chyba při načítání zemí:', error);
            });
    }

    createCountryMarkersFromLatLon(countryData) {
        countryData.forEach(country => {
            // Výpočet theta a phi z lat/lon
            const phi = (90 - country.lat) * (Math.PI / 180);
            const theta = (country.lon) * (Math.PI / 180);

            const x = -(1.02 * Math.sin(phi) * Math.cos(theta));
            const z = (1.02 * Math.sin(phi) * Math.sin(theta));
            const y = (1.02 * Math.cos(phi));

            const markerGeometry = new THREE.SphereGeometry(0.015, 16, 16);
            const markerMaterial = new THREE.MeshBasicMaterial({
                color: 0x000000,
                transparent: true,
                opacity: 1.0
            });
            const marker = new THREE.Mesh(markerGeometry, markerMaterial);
            marker.position.set(x, y, z);

            marker.userData = {
                name: country.name,
                lat: country.lat,
                lon: country.lon,
                theta: theta,
                phi: phi,
                population: country.population || 'N/A',
                capital: country.capital || 'N/A'
            };

            this.globe.add(marker);
            this.countries.push(marker);

            console.log(`✓ ${country.name}: lat=${country.lat}°, lon=${country.lon}°`);
        });

        console.log(`========================================`);
        console.log(`✓ Zobrazeno ${this.countries.length} zemí`);
        console.log(`========================================`);
    }

    latLonToVector3(lat, lon, radius) {
        // Správné mapování lat/lon na sphere
        const phi = (90 - lat) * (Math.PI / 180);
        const theta = (180 - lon) * (Math.PI / 180);

        const x = -(radius * Math.sin(phi) * Math.cos(theta));
        const z = (radius * Math.sin(phi) * Math.sin(theta));
        const y = (radius * Math.cos(phi));

        return new THREE.Vector3(x, y, z);
    }

    addEventListeners() {
        this.renderer.domElement.addEventListener('mousemove', (event) => this.onMouseMove(event));
        this.renderer.domElement.addEventListener('click', (event) => this.onClick(event));
        document.addEventListener('keydown', (event) => this.onKeyDown(event));
    }

    onMouseMove(event) {
        const rect = this.renderer.domElement.getBoundingClientRect();
        this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        this.checkIntersection();
    }

    onKeyDown(event) {
        if (!this.selectedMarker) return;

        const step = event.shiftKey ? 5 : 1; // Shift = větší krok
        let changed = false;

        switch(event.key) {
            case 'ArrowUp':
                this.selectedMarker.userData.lat += step;
                changed = true;
                break;
            case 'ArrowDown':
                this.selectedMarker.userData.lat -= step;
                changed = true;
                break;
            case 'ArrowLeft':
                this.selectedMarker.userData.lon -= step;
                changed = true;
                break;
            case 'ArrowRight':
                this.selectedMarker.userData.lon += step;
                changed = true;
                break;
            case 'Escape':
                this.deselectMarker();
                return;
        }

        if (changed) {
            event.preventDefault();
            this.updateMarkerPosition(this.selectedMarker);
            console.log(`${this.selectedMarker.userData.name}: lat=${this.selectedMarker.userData.lat.toFixed(2)}°, lon=${this.selectedMarker.userData.lon.toFixed(2)}°`);
        }
    }

    updateMarkerPosition(marker) {
        // Přepočítat 3D pozici z lat/lon
        const phi = (90 - marker.userData.lat) * (Math.PI / 180);
        const theta = (marker.userData.lon) * (Math.PI / 180);

        const x = -(1.02 * Math.sin(phi) * Math.cos(theta));
        const z = (1.02 * Math.sin(phi) * Math.sin(theta));
        const y = (1.02 * Math.cos(phi));

        marker.position.set(x, y, z);

        // Aktualizovat info panel
        if (this.selectedMarker === marker) {
            this.showCountryInfo(marker.userData);
        }
    }

    onClick(event) {
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.countries);

        if (intersects.length > 0) {
            const marker = intersects[0].object;

            // Pokud klikneš na již vybraný marker, zobraz možnost exportu
            if (this.selectedMarker === marker) {
                const input = prompt(`Země: ${marker.userData.name}\n\nZadej "export" pro export všech dat\nNebo stiskni Enter`);

                if (input && input.toLowerCase() === 'export') {
                    this.exportCountryData();
                    return;
                }
            } else {
                // Vyber nový marker
                this.selectMarker(marker);
            }
        } else {
            // Kliknutí mimo - deselect
            this.deselectMarker();
        }
    }

    selectMarker(marker) {
        // Zrušit předchozí výběr
        if (this.selectedMarker) {
            this.selectedMarker.material.emissive.setHex(0x000000);
        }

        // Vybrat nový marker
        this.selectedMarker = marker;
        this.selectedMarker.material.emissive.setHex(0x444444);

        console.log(`\n========================================`);
        console.log(`VYBRÁNA: ${marker.userData.name}`);
        console.log(`Pozice: lat=${marker.userData.lat.toFixed(2)}°, lon=${marker.userData.lon.toFixed(2)}°`);
        console.log(`========================================`);
        console.log('OVLÁDÁNÍ:');
        console.log('  ↑ ↓ ← → : Posun o 1°');
        console.log('  Shift + šipky: Posun o 5°');
        console.log('  ESC: Zrušit výběr');
        console.log('  Klikni znovu na zemi: Export dat');
        console.log(`========================================\n`);

        this.showCountryInfo(marker.userData);
    }

    deselectMarker() {
        if (this.selectedMarker) {
            this.selectedMarker.material.emissive.setHex(0x000000);
            this.selectedMarker = null;
            this.hideCountryInfo();
            console.log('Výběr zrušen');
        }
    }

    getAssignedCount() {
        return this.countries.filter(m => m.userData.assigned).length;
    }

    exportCountryData() {
        const allCountries = this.countries.map(m => ({
            name: m.userData.name,
            lat: Math.round(m.userData.lat * 100) / 100,  // Zaokrouhlit na 2 des. místa
            lon: Math.round(m.userData.lon * 100) / 100
        }));

        console.log('========================================');
        console.log('=== EXPORT VŠECH ZEMÍ (UPRAVENO) ===');
        console.log('========================================');
        console.log(JSON.stringify(allCountries, null, 2));
        console.log('========================================');
        console.log(`Celkem: ${allCountries.length} zemí`);
        console.log('Zkopíruj JSON výše a pošli mi ho!');
        console.log('========================================');

        alert(`✓ Exportováno ${allCountries.length} zemí do konzole (F12)\n\nZkopíruj JSON a pošli mi ho!`);
    }

    checkIntersection() {
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.countries);

        // Reset všech markerů
        this.countries.forEach(marker => {
            marker.material.color.setHex(0x000000);
            marker.material.opacity = 1.0;
            marker.scale.set(1, 1, 1);

            // Vybraný marker má emissive glow
            if (marker === this.selectedMarker) {
                marker.material.emissive.setHex(0x444444);
            } else {
                marker.material.emissive.setHex(0x000000);
            }
        });

        if (intersects.length > 0) {
            const intersected = intersects[0].object;

            // Pouze zvýraznit pokud NENÍ vybraný
            if (intersected !== this.selectedMarker) {
                intersected.material.color.setHex(0xff6b6b);
                intersected.scale.set(1.5, 1.5, 1.5);
            }

            this.renderer.domElement.style.cursor = 'pointer';
        } else {
            this.renderer.domElement.style.cursor = 'grab';
        }
    }

    showMarkerInfo(markerData) {
        const infoPanel = document.getElementById('country-info');
        const countryName = document.getElementById('country-name');
        const countryPopulation = document.getElementById('country-population');
        const countryCapital = document.getElementById('country-capital');

        countryName.textContent = 'Nepřiřazený bod';
        countryPopulation.textContent = `Lat: ${markerData.lat}°, Lon: ${markerData.lon}°`;
        countryCapital.textContent = 'Klikni pro přiřazení země';

        infoPanel.classList.remove('hidden');
    }

    showCountryInfo(countryData) {
        const infoPanel = document.getElementById('country-info');
        const countryName = document.getElementById('country-name');
        const countryPopulation = document.getElementById('country-population');
        const countryCapital = document.getElementById('country-capital');

        countryName.textContent = countryData.name;
        countryPopulation.textContent = `Lat: ${countryData.lat}°, Lon: ${countryData.lon}°`;
        countryCapital.textContent = countryData.capital || 'Klikni pro změnu';

        infoPanel.classList.remove('hidden');
    }

    hideCountryInfo() {
        const infoPanel = document.getElementById('country-info');
        infoPanel.classList.add('hidden');
    }

    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
}
