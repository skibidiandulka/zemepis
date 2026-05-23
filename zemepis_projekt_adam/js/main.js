// Main.js - Hlavní inicializace aplikace

document.addEventListener('DOMContentLoaded', () => {
    console.log('Inicializace aplikace pro vizualizaci parlamentních voleb...');

    // Vytvoření instance Globe
    const globe = new Globe('globe-container');

    console.log('Zeměkoule inicializována!');
    console.log('Ovládání:');
    console.log('- Levé tlačítko myši: otáčení');
    console.log('- Kolečko myši: zoom');
    console.log('- Najetí myší na značku: zobrazení informací o zemi');
});
