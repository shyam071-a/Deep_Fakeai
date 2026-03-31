// Sare UI elements ko select karein
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const scanner = document.getElementById('scanner');
const fileInfo = document.getElementById('fileInfo');

// Jab dropzone par click ho toh file selector khule
dropZone.onclick = () => fileInput.click();

// Jab file select ho jaye toh uska naam dikhayein
fileInput.onchange = (e) => {
    if (e.target.files.length > 0) {
        const fileName = e.target.files[0].name;
        fileInfo.innerText = `Selected: ${fileName}`;
        fileInfo.style.color = "#00f2fe"; // Neon blue color for selection
    }
};

// Main Function: Analysis start karne ke liye
analyzeBtn.onclick = async () => {
    // Check karein ki file select hui hai ya nahi
    if (!fileInput.files[0]) {
        return alert("Please select a file first.");
    }

    // 1. UI Updates (Processing Mode)
    scanner.style.display = 'block'; // Scan line dikhayein
    analyzeBtn.innerText = "Analyzing Neural Patterns...";
    analyzeBtn.disabled = true;

    // 2. Data pack karein (Python ko bhejne ke liye)
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        // 3. Python Backend (Flask) ko request bhejna
        // Note: Hum relative path '/analyze' use kar rahe hain kyunki frontend-backend same server par hain
        const response = await fetch('/analyze', { 
            method: 'POST', 
            body: formData 
        });

        if (!response.ok) throw new Error("Server error");

        const data = await response.json();

        // 4. Results Reveal (UI ko update karna)
        document.querySelector('.placeholder-text').style.display = 'none';
        const resultsArea = document.querySelector('.actual-results');
        resultsArea.style.display = 'block';
        scanner.style.display = 'none'; // Scan khatam
        
        // Status update (Fake = Red, Real = Blue)
        const statusEl = document.getElementById('resultStatus');
        statusEl.innerText = data.status;
        statusEl.style.color = (data.status === 'Fake') ? '#ff4b2b' : '#00f2fe';
        
        // Confidence bar aur percentage update
        document.getElementById('confValue').innerText = `${data.confidence}%`;
        document.getElementById('confFill').style.width = `${data.confidence}%`;
        
        // Detailed text update
        document.getElementById('shortDiff').innerText = data.short_diff;
        document.getElementById('detailedExp').innerText = data.explanation;

    } catch (err) {
        console.error(err);
        alert("Error: Backend se connect nahi ho paya. Pehle 'python app.py' run karein.");
        scanner.style.display = 'none';
    } finally {
        // 5. Button ko reset karein
        analyzeBtn.innerText = "Start Deep Analysis";
        analyzeBtn.disabled = false;
    }
};
