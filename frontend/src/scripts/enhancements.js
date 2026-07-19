/* =============================================================================
   Rashid Dental — Enhancements Script
   Custom Cursor | Vanta 3D | AOS | Voice Feature
   ============================================================================= */

(function () {
  'use strict';

  // ─────────────────────────────────────────────
  // 1. CUSTOM CURSOR
  // ─────────────────────────────────────────────
  var dot  = document.getElementById('cursor-dot');
  var ring = document.getElementById('cursor-ring');
  var mouseX = 0, mouseY = 0;
  var ringX  = 0, ringY  = 0;

  if (dot && ring && window.matchMedia('(pointer: fine)').matches) {
    document.addEventListener('mousemove', function (e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.left = mouseX + 'px';
      dot.style.top  = mouseY + 'px';
    });

    // Smooth ring follow
    function animateRing() {
      ringX += (mouseX - ringX) * 0.12;
      ringY += (mouseY - ringY) * 0.12;
      ring.style.left = ringX + 'px';
      ring.style.top  = ringY + 'px';
      requestAnimationFrame(animateRing);
    }
    animateRing();

    // Hover effect on interactive elements
    var hoverTargets = 'a, button, input, textarea, [data-tilt]';
    document.querySelectorAll(hoverTargets).forEach(function (el) {
      el.addEventListener('mouseenter', function () { ring.classList.add('hovering'); });
      el.addEventListener('mouseleave', function () { ring.classList.remove('hovering'); });
    });

    // Hide when leaving window
    document.addEventListener('mouseleave', function () {
      dot.style.opacity  = '0';
      ring.style.opacity = '0';
    });
    document.addEventListener('mouseenter', function () {
      dot.style.opacity  = '1';
      ring.style.opacity = '0.6';
    });
  }

  // ─────────────────────────────────────────────
  // 2. VANTA.JS — 3D Animated Waves Background
  // ─────────────────────────────────────────────
  if (typeof VANTA !== 'undefined' && document.getElementById('vanta-bg')) {
    VANTA.WAVES({
      el: '#vanta-bg',
      THREE: THREE,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.0,
      minWidth: 200.0,
      scale: 1.0,
      scaleMobile: 1.0,
      color: 0x0a1628,
      shininess: 30.0,
      waveHeight: 18.0,
      waveSpeed: 0.6,
      zoom: 0.85,
    });
  }

  // ─────────────────────────────────────────────
  // 3. AOS — Scroll Reveal Animations
  // ─────────────────────────────────────────────
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 700,
      easing: 'ease-out-cubic',
      once: true,
      offset: 60,
    });
  }

  // ─────────────────────────────────────────────
  // 4. VANILLA TILT — init is auto if data-tilt attr set
  //    But we also do manual init for safety
  // ─────────────────────────────────────────────
  if (typeof VanillaTilt !== 'undefined') {
    VanillaTilt.init(document.querySelectorAll('[data-tilt]'), {
      max: 8,
      speed: 400,
      glare: true,
      'max-glare': 0.1,
      perspective: 1200,
    });
  }

  // ─────────────────────────────────────────────
  // 5. VOICE INPUT — Web Speech API
  // ─────────────────────────────────────────────
  var voiceBtn    = document.getElementById('chatbot-voice');
  var voiceStatus = document.getElementById('voice-status');
  var chatInput   = document.getElementById('chatbot-input');

  if (voiceBtn && ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    var recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    var isListening = false;

    voiceBtn.addEventListener('click', function () {
      if (isListening) {
        recognition.stop();
      } else {
        recognition.start();
      }
    });

    recognition.onstart = function () {
      isListening = true;
      voiceBtn.classList.add('listening');
      if (voiceStatus) {
        voiceStatus.classList.add('visible');
      }
    };

    recognition.onresult = function (event) {
      var transcript = '';
      for (var i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      if (chatInput) {
        chatInput.value = transcript;
      }
    };

    recognition.onend = function () {
      isListening = false;
      voiceBtn.classList.remove('listening');
      if (voiceStatus) {
        voiceStatus.classList.remove('visible');
      }
      // Auto send if there is text
      var sendBtn = document.getElementById('chatbot-send');
      if (chatInput && chatInput.value.trim() && sendBtn) {
        setTimeout(function () { sendBtn.click(); }, 300);
      }
    };

    recognition.onerror = function (event) {
      isListening = false;
      voiceBtn.classList.remove('listening');
      if (voiceStatus) {
        voiceStatus.classList.remove('visible');
      }
      if (event.error === 'not-allowed') {
        alert('Microphone access denied. Please allow microphone permissions in your browser.');
      }
    };

  } else if (voiceBtn) {
    // Browser doesn't support — hide the button
    voiceBtn.style.display = 'none';
  }

})();
