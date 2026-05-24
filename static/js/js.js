/* ==========================================================================
   Government of Rajasthan — Internship & E-Governance Portal
   Client-Side Interaction & Machine Learning Mock Execution Engine
   ========================================================================== */

// ── CLOCK SYNCHRONIZATION ENGINE ──
function initLiveClock() {
    function updateTime() {
        const now = new Date();
        const options = { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' };
        const dateString = now.toLocaleDateString('en-IN', options);
        const timeString = now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const consolidatedTimestamp = `${dateString} | ${timeString}`;
        
        const topDisplay = document.getElementById('datetime-display');
        const footerDisplay = document.getElementById('footer-datetime');
        
        if (topDisplay) topDisplay.textContent = consolidatedTimestamp;
        if (footerDisplay) footerDisplay.textContent = consolidatedTimestamp;
    }
    updateTime();
    setInterval(updateTime, 1000);
}

// ── OVERLAY INTERACTIVE WINDOW MANAGERS ──
function showModal(modalId) {
    const targetModal = document.getElementById(modalId);
    if (targetModal) targetModal.classList.add('open');
}

function closeModal(modalId) {
    const targetModal = document.getElementById(modalId);
    if (targetModal) targetModal.classList.remove('open');
}

// ── STATUS ALERT TOAST NOTIFIER ──
function showToast(message, visualType) {
    const targetContainer = document.getElementById('toast-container');
    if (!targetContainer) return;
    
    const toastElement = document.createElement('div');
    toastElement.className = `toast ${visualType || ''}`;
    toastElement.innerHTML = `<span>${message}</span>`;
    targetContainer.appendChild(toastElement);
    
    setTimeout(() => {
        toastElement.style.opacity = '0';
        toastElement.style.transform = 'translateX(100%)';
        toastElement.style.transition = 'all 0.3s ease';
        setTimeout(() => toastElement.remove(), 300);
    }, 3200);
}

// ── MACHINE LEARNING ANCHORED PREDICTION MODEL ──
function runMLPredict() {
    const cgpaElement = document.getElementById('ml-cgpa');
    const attendanceElement = document.getElementById('ml-att');
    const skillElement = document.getElementById('ml-skill');
    const streamElement = document.getElementById('ml-stream');
    
    if (!cgpaElement || !attendanceElement || !skillElement) return;

    const cgpa = parseFloat(cgpaElement.value) || 0;
    const attendance = parseFloat(attendanceElement.value) || 0;
    const technicalSkills = parseFloat(skillElement.value) || 0;
    const streamValue = streamElement ? streamElement.value : 'cs';

    // Algorithmic weighting model variables
    const weights = { cs: 0.15, commerce: 0.08, mech: 0.02, civil: 0, science: 0.04 };
    const baseCumulativeValue = (cgpa / 10) * 0.4 + (attendance / 100) * 0.35 + (technicalSkills / 10) * 0.25;
    const boundedProbability = Math.min(0.98, baseCumulativeValue + (weights[streamValue] || 0));
    const percentageScore = Math.round(boundedProbability * 100);

    let hexColor, classificationLabel, technicalAdvice;
    if (percentageScore >= 75) {
        hexColor = '#1b5e20';
        classificationLabel = 'High Placement Probability';
        technicalAdvice = 'Student profile is highly viable. Prioritize custom mock interview runs.';
    } else if (percentageScore >= 50) {
        hexColor = '#e65c00';
        classificationLabel = 'Moderate Placement Probability';
        technicalAdvice = 'Strengthen core certification frameworks and secure target attendance thresholds.';
    } else {
        hexColor = '#b71c1c';
        classificationLabel = 'Low Placement Probability';
        technicalAdvice = 'Immediate counseling intervention and standard skill patch tracks required.';
    }

    const resultBox = document.getElementById('ml-result');
    if (!resultBox) return;
    
    resultBox.style.display = 'block';
    resultBox.innerHTML = `
        <div style="border:2px solid ${hexColor}; border-radius:4px; padding:12px; background: #fff;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <strong style="font-size:14px; color:${hexColor};">${percentageScore}% — ${classificationLabel}</strong>
                <span class="badge" style="background:${hexColor}20; color:${hexColor}; border:1px solid ${hexColor}40;">Model v1.2</span>
            </div>
            <div style="background:#f0f0f0; border-radius:3px; height:10px; overflow:hidden; margin-bottom:8px;">
                <div style="width:${percentageScore}%; height:100%; background:${hexColor}; transition:width 0.5s ease-out;"></div>
            </div>
            <div style="font-size:12px; color:#444;">⚠ ${technicalAdvice}</div>
        </div>`;
}

// ── RUN SYSTEM LIFECYCLE LISTENERS ──
document.addEventListener('DOMContentLoaded', () => {
    initLiveClock();
    
    // Close modal structures securely if background overlays are clicked
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', function(event) {
            if (event.target === this) this.classList.remove('open');
        });
    });
});