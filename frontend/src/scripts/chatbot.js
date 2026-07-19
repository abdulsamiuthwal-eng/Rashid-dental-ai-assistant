(function () {
  const API_BASE = '/api/v1';

  const SUGGESTED_QUESTIONS = [
    'What services do you provide?',
    'What are your opening hours?',
    'How do I book an appointment?',
    'Where is the clinic located?',
  ];

  const state = {
    sessionId: null,
    isOpen: false,
    isProcessing: false,
  };

  let messagesContainer;
  let inputField;
  let sendBtn;
  let trigger;
  let windowEl;
  let suggestionsEl;
  let errorEl;
  let typingEl;

  function init() {
    trigger = document.getElementById('chatbot-trigger');
    windowEl = document.getElementById('chatbot-window');
    messagesContainer = document.getElementById('chatbot-messages');
    inputField = document.getElementById('chatbot-input');
    sendBtn = document.getElementById('chatbot-send');
    suggestionsEl = document.getElementById('chatbot-suggestions');
    errorEl = document.getElementById('chatbot-error');

    if (!trigger || !windowEl) return;

    trigger.addEventListener('click', toggleChatbot);
    sendBtn.addEventListener('click', handleSend);
    inputField.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    });

    document.getElementById('chatbot-close')?.addEventListener('click', closeChatbot);
    document.getElementById('chatbot-restart')?.addEventListener('click', restartChat);

    renderSuggestedQuestions();

    setTimeout(function () {
      if (!state.isOpen) {
        trigger.classList.add('pulse');
        setTimeout(function () { trigger.classList.remove('pulse'); }, 2000);
      }
    }, 5000);
  }

  function toggleChatbot() {
    if (state.isOpen) {
      closeChatbot();
    } else {
      openChatbot();
    }
  }

  function openChatbot() {
    state.isOpen = true;
    windowEl.classList.add('open');
    trigger.classList.add('active');
    trigger.setAttribute('aria-label', 'Close chat');

    if (!state.sessionId) {
      addWelcomeMessage();
    }

    setTimeout(function () { inputField.focus(); }, 400);
  }

  function closeChatbot() {
    state.isOpen = false;
    windowEl.classList.remove('open');
    trigger.classList.remove('active');
    trigger.setAttribute('aria-label', 'Open chat');
  }

  function restartChat() {
    state.sessionId = null;
    state.isProcessing = false;
    messagesContainer.innerHTML = '';
    hideError();
    addWelcomeMessage();
  }

  function addWelcomeMessage() {
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'message assistant welcome-message';
    welcomeDiv.innerHTML =
      '<strong>Hello! I\'m the Rashid Dental AI Assistant.</strong><br><br>' +
      'I\'m here to help you with information about our clinic, services, and to assist with appointment requests. ' +
      'Please note that I\'m an AI — not a dentist — so for any medical concerns, our dental team is always the best resource.' +
      '<br><br>How can I help you today?';

    messagesContainer.appendChild(welcomeDiv);

    const contactBtn = document.createElement('button');
    contactBtn.className = 'contact-clinic-btn';
    contactBtn.textContent = '📞 Contact the clinic directly';
    contactBtn.addEventListener('click', function () {
      document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' });
    });
    welcomeDiv.appendChild(contactBtn);

    autoScroll();
  }

  function renderSuggestedQuestions() {
    if (!suggestionsEl) return;
    suggestionsEl.innerHTML = '';
    SUGGESTED_QUESTIONS.forEach(function (q) {
      const btn = document.createElement('button');
      btn.textContent = q;
      btn.addEventListener('click', function () {
        inputField.value = q;
        handleSend();
      });
      suggestionsEl.appendChild(btn);
    });
  }

  function handleSend() {
    const message = inputField.value.trim();
    if (!message) return;
    if (state.isProcessing) return;

    inputField.value = '';
    hideError();
    addUserMessage(message);
    sendToAPI(message);
  }

  function addUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'message user';
    div.textContent = text;
    messagesContainer.appendChild(div);
    autoScroll();
  }

  function addAssistantMessage(text, sources) {
    removeTyping();

    const div = document.createElement('div');
    div.className = 'message assistant';
    div.textContent = text;

    if (sources && sources.length > 0) {
      const sourceDiv = document.createElement('div');
      sourceDiv.className = 'message-source';
      sourceDiv.innerHTML = '<span><strong>Sources:</strong></span>';
      sources.forEach(function (s) {
        sourceDiv.innerHTML += '<span>' + escapeHtml(s.filename) + ' — ' + escapeHtml(s.heading) + '</span>';
      });
      div.appendChild(sourceDiv);
    }

    messagesContainer.appendChild(div);
    autoScroll();
  }

  function showTyping() {
    typingEl = document.createElement('div');
    typingEl.className = 'typing-indicator';
    typingEl.innerHTML = '<span></span><span></span><span></span>';
    messagesContainer.appendChild(typingEl);
    autoScroll();
  }

  function removeTyping() {
    if (typingEl && typingEl.parentNode) {
      typingEl.parentNode.removeChild(typingEl);
      typingEl = null;
    }
  }

  function showError(message) {
    if (!errorEl) return;
    errorEl.textContent = message;
    errorEl.style.display = 'block';
  }

  function hideError() {
    if (!errorEl) return;
    errorEl.style.display = 'none';
  }

  function autoScroll() {
    requestAnimationFrame(function () {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });
  }

  function sendToAPI(message) {
    state.isProcessing = true;
    sendBtn.disabled = true;
    showTyping();

    var body = JSON.stringify({
      message: message,
      session_id: state.sessionId,
    });

    fetch(API_BASE + '/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body,
    })
      .then(function (res) {
        if (!res.ok) {
          if (res.status === 503) throw new Error('Service unavailable');
          if (res.status === 422) throw new Error('Invalid input');
          throw new Error('Server error');
        }
        return res.json();
      })
      .then(function (data) {
        state.sessionId = data.session_id;
        addAssistantMessage(data.message, data.sources);
      })
      .catch(function (err) {
        removeTyping();
        if (err.message === 'Failed to fetch' || err.message === 'NetworkError') {
          showError('Unable to connect to the server. Please make sure the backend is running.');
          addAssistantMessage(
            'I apologize, but I am currently unable to connect to my services. Please ensure the server is running, or try again later. You can also contact Rashid Dental Clinic directly for assistance.'
          );
        } else {
          showError('Something went wrong. Please try again or contact the clinic directly.');
          addAssistantMessage(
            'I apologize, but I encountered an error processing your request. Please try again, or contact Rashid Dental Clinic directly for assistance.'
          );
        }
      })
      .finally(function () {
        state.isProcessing = false;
        sendBtn.disabled = false;
      });
  }

  function escapeHtml(text) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
