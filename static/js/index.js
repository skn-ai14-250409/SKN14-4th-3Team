// 전역 변수
let conversations = {
  1: {
    title: "대화-1",
    messages: [],
    image: null,
  },
};
let currentConversationId = "1";
let isTyping = false;

// DOM 요소
const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
const chatForm = document.getElementById("chatForm");
const imageInput = document.getElementById("imageInput");
const attachBtn = document.getElementById("attachBtn");
const imageDisplayArea = document.getElementById("imageDisplayArea");
const conversationList = document.getElementById("conversationList");
const newChatBtn = document.getElementById("newChatBtn");
const clearAllBtn = document.getElementById("clearAllBtn");
const deleteCurrBtn = document.getElementById("deleteCurrBtn");
const downloadBtn = document.getElementById("downloadBtn");
const downloadCurrBtn = document.getElementById("downloadCurrBtn");
const totalMessages = document.getElementById("totalMessages");
const totalConversations = document.getElementById("totalConversations");
const typingIndicator = document.getElementById("typingIndicator");
const currentChannelTitle = document.getElementById("currentChannelTitle");
const imagePreviewContainer = document.getElementById("imagePreviewContainer");
const imagePreview = document.getElementById("imagePreview");
const imageName = document.getElementById("imageName");
const imageSize = document.getElementById("imageSize");
const removeImage = document.getElementById("removeImage");

// 초기화
document.addEventListener("DOMContentLoaded", function () {
  updateChatDisplay();
  updateStats();
  setupEventListeners();
});

// 이벤트 리스너 설정
function setupEventListeners() {
  // 채팅 폼 제출
  chatForm.addEventListener("submit", handleChatSubmit);

  // 이미지 업로드
  attachBtn.addEventListener("click", () => imageInput.click());
  imageInput.addEventListener("change", handleImageUpload);
  
  // 이미지 제거
  if (removeImage) {
    removeImage.addEventListener("click", removeUploadedImage);
  }

  // 버튼 이벤트
  newChatBtn.addEventListener("click", createNewConversation);
  clearAllBtn.addEventListener("click", clearAllConversations);
  deleteCurrBtn.addEventListener("click", deleteCurrentConversation);
  downloadBtn.addEventListener("click", downloadChatHistory);
  downloadCurrBtn.addEventListener("click", downloadChatCurrHistory);
  
  // 엔터키로 전송
  messageInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chatForm.dispatchEvent(new Event("submit"));
    }
  });
}

// 채팅 제출 처리
async function handleChatSubmit(e) {
  e.preventDefault();
  const message = messageInput.value.trim();
  const OriginConvId = currentConversationId;
  const currentConv = conversations[OriginConvId];

  if (!message && !currentConv.image) return;

  if (message) {
    addMessage("user", message);
    messageInput.value = "";
  }

  // 서버 연동
  const history = currentConv.messages
    .map((m) => ({ role: m.role, content: m.content }));

  showTypingIndicator();
  try {
    const response = await sendChatQuery(message, history);
    hideTypingIndicator();

    const reply = response.response || "응답을 불러오지 못했습니다.";

    if (OriginConvId === currentConversationId) {
      addMessage("assistant", reply);
    } else {
      conversations[OriginConvId].messages.push({
        role: "assistant",
        content: reply,
        timestamp: new Date(),
        author: "Q&A Bot"
      });
    }

    updateStats();
  } catch (error) {
    hideTypingIndicator();
    const errorMsg = "서버 오류가 발생했습니다. 다시 시도해주세요.";

    if (OriginConvId === currentConversationId) {
      addMessage("assistant", errorMsg);
    } else {
      conversations[OriginConvId].messages.push({
        role: "assistant",
        content: errorMsg,
        timestamp: new Date(),
        author: "Q&A Bot"
      });
    }

    console.error("Chat API error:", error);
  }
}

// 메시지 추가
function addMessage(role, content) {
  const author = role === "user" ? "사용자" : "Q&A Bot";
  conversations[currentConversationId].messages.push({
    role: role,
    content: content,
    timestamp: new Date(),
    author: author
  });
  updateChatDisplay();
  updateStats();
  scrollToBottom();
}

// 타이핑 인디케이터
function showTypingIndicator() {
  if (typingIndicator) {
    typingIndicator.style.display = "flex";
  }
  
  // 메시지 영역에도 타이핑 표시 추가
  const typingDiv = document.createElement("div");
  typingDiv.className = "message bot typing-message";
  typingDiv.innerHTML = `
    <div class="avatar bot">🤖</div>
    <div class="message-content">
      <div class="message-header">
        <span class="message-author">Q&A Bot</span>
        <span class="message-timestamp">${formatTime(new Date())}</span>
      </div>
      <div class="typing-indicator">
        답변을 작성 중입니다<span class="typing-dots"></span>
      </div>
    </div>
  `;
  chatMessages.appendChild(typingDiv);
  scrollToBottom();
}

function hideTypingIndicator() {
  if (typingIndicator) {
    typingIndicator.style.display = "none";
  }
  
  const typingMessage = chatMessages.querySelector(".typing-message");
  if (typingMessage) {
    typingMessage.remove();
  }
}

// HTML 이스케이프
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// 메시지 컨텐츠 포맷팅
function formatMessageContent(content) {
  const escaped = escapeHtml(content);
  
  const lines = escaped.split("\n").map(line => {
    if (line.startsWith("### ")) return `<h3>${line.slice(4)}</h3>`;
    if (line.startsWith("## ")) return `<h2>${line.slice(3)}</h2>`;
    if (line.startsWith("# ")) return `<h1>${line.slice(2)}</h1>`;
    return line;
  });
  
  return lines.join("<br>");
}

// 시간 포맷팅
function formatTime(date) {
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  return `오늘 ${hours}:${minutes}`;
}

// 채팅 화면 업데이트
function updateChatDisplay() {
  const messages = conversations[currentConversationId].messages;
  
  // 환영 메시지와 날짜 구분선 유지
  const existingWelcome = chatMessages.querySelector('.welcome-message');
  const existingDivider = chatMessages.querySelector('.date-divider');
  
  chatMessages.innerHTML = "";
  
  // 환영 메시지 복원
  if (existingWelcome || messages.length === 0) {
    chatMessages.innerHTML = `
      <div class="welcome-message">
        <div class="welcome-icon">🧺</div>
        <h2>${conversations[currentConversationId].title}에 오신 것을 환영합니다!</h2>
        <p>세탁기/건조기 매뉴얼 Q&A 챗봇이 시작되었습니다.</p>
      </div>
      <div class="date-divider">
        <span>오늘</span>
      </div>
    `;
  }

  messages.forEach((message) => {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${message.role}`;
    
    const avatar = message.role === "user" ? "👤" : "🤖";
    const formattedContent = formatMessageContent(message.content);
    
    messageDiv.innerHTML = `
      <div class="avatar ${message.role}">${avatar}</div>
      <div class="message-content">
        <div class="message-header">
          <span class="message-author">${message.author || (message.role === "user" ? "사용자" : "Q&A Bot")}</span>
          <span class="message-timestamp">${formatTime(message.timestamp || new Date())}</span>
        </div>
        <div class="message-text">${formattedContent}</div>
      </div>
    `;
    
    chatMessages.appendChild(messageDiv);
  });

  scrollToBottom();
  updateImageDisplay();
}

// 이미지 업로드 처리
function handleImageUpload(e) {
  const file = e.target.files[0];
  if (file) {
    processImage(file);
  }
}

// 이미지 처리
function processImage(file) {
  const reader = new FileReader();
  reader.onload = async function (e) {
    conversations[currentConversationId].image = {
      src: e.target.result,
      name: file.name,
      size: file.size
    };
    
    // 미리보기 표시
    showImagePreview(e.target.result, file.name, file.size);
    
    addMessage("user", `이미지를 업로드했습니다: ${file.name}`);

    try {
      const result = await uploadImageAndGetModelCode(file);
      const modelInfo = result.model_code || "모델 정보를 찾을 수 없습니다.";
      addMessage("assistant", `이미지 분석 결과: ${modelInfo}`);
    } catch (err) {
      console.error("Image upload error:", err);
      addMessage("assistant", "이미지 분석 중 오류가 발생했습니다.");
    }
  };
  reader.readAsDataURL(file);
}

// 이미지 미리보기 표시
function showImagePreview(src, name, size) {
  if (imagePreviewContainer) {
    imagePreview.src = src;
    imageName.textContent = name;
    imageSize.textContent = formatFileSize(size);
    imagePreviewContainer.style.display = "block";
  }
  updateImageDisplay();
}

// 업로드된 이미지 제거
function removeUploadedImage() {
  conversations[currentConversationId].image = null;
  if (imagePreviewContainer) {
    imagePreviewContainer.style.display = "none";
  }
  updateImageDisplay();
}

// 파일 사이즈 포맷
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// 이미지 표시 업데이트
function updateImageDisplay() {
  const currentImage = conversations[currentConversationId].image;

  if (currentImage) {
    imageDisplayArea.innerHTML = `
      <img src="${currentImage.src}" alt="업로드된 이미지" class="uploaded-image">
    `;
  } else {
    imageDisplayArea.innerHTML = `
      <div class="no-image">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor" opacity="0.3">
          <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
        </svg>
        <p>이미지가 없습니다</p>
      </div>
    `;
  }
}

// 새 대화 생성
function createNewConversation() {
  const newId = String(
    Math.max(...Object.keys(conversations).map((k) => parseInt(k))) + 1
  );
  conversations[newId] = {
    title: `대화-${newId}`,
    messages: [],
    image: null,
  };
  currentConversationId = newId;
  updateConversationList();
  updateChatDisplay();
  updateStats();
  
  // 채널 제목 업데이트
  if (currentChannelTitle) {
    currentChannelTitle.textContent = conversations[newId].title;
  }
}

// 대화 목록 업데이트
function updateConversationList() {
  conversationList.innerHTML = "";
  Object.keys(conversations).forEach((id) => {
    const channelDiv = document.createElement("div");
    channelDiv.className = `channel-item ${id === currentConversationId ? "active" : ""}`;
    channelDiv.setAttribute("data-id", id);
    channelDiv.innerHTML = `
      <span class="channel-hash">#</span>
      <span class="channel-name">${conversations[id].title}</span>
    `;
    channelDiv.addEventListener("click", () => switchConversation(id));
    conversationList.appendChild(channelDiv);
  });
}

// 대화 전환
function switchConversation(id) {
  currentConversationId = id;
  updateConversationList();
  updateChatDisplay();
  
  // 채널 제목 업데이트
  if (currentChannelTitle) {
    currentChannelTitle.textContent = conversations[id].title;
  }
  
  // 이미지 미리보기 업데이트
  const currentImage = conversations[id].image;
  if (currentImage && imagePreviewContainer) {
    showImagePreview(currentImage.src, currentImage.name, currentImage.size);
  } else if (imagePreviewContainer) {
    imagePreviewContainer.style.display = "none";
  }
}

// 모든 대화 삭제
function clearAllConversations() {
  if (confirm("정말로 모든 대화 기록을 삭제하시겠습니까?")) {
    conversations = {
      1: {
        title: "대화-1",
        messages: [],
        image: null,
      },
    };
    currentConversationId = "1";
    updateConversationList();
    updateChatDisplay();
    updateStats();
  }
}

// 현재 대화 삭제
function deleteCurrentConversation() {
  if (confirm("정말로 현재 대화를 삭제하시겠습니까?")) {
    delete conversations[currentConversationId];

    const remainingIds = Object.keys(conversations);
    if (remainingIds.length > 0) {
      currentConversationId = remainingIds.sort((a, b) => parseInt(a) - parseInt(b))[0];
    } else {
      currentConversationId = "1";
      conversations[currentConversationId] = {
        title: "대화-1",
        messages: [],
        image: null,
      };
    }

    updateConversationList();
    updateChatDisplay();
    updateStats();
  }
}

// 채팅 기록 다운로드
function downloadChatHistory() {
  const data = {
    conversations: conversations,
    downloadDate: new Date().toISOString(),
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `chat_history_${new Date()
    .toISOString()
    .slice(0, 19)
    .replace(/:/g, "-")}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

// 현재 대화 기록만 다운로드
function downloadChatCurrHistory() {
  const currConv = conversations[currentConversationId];
  if (!currConv) {
    alert("현재 대화 기록이 없습니다.");
    return;
  }

  const data = {
    title: currConv.title,
    messages: currConv.messages,
    image: currConv.image,
    downloadDate: new Date().toISOString(),
  };

  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });

  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `chat_${currentConversationId}_${new Date()
    .toISOString()
    .slice(0, 19)
    .replace(/:/g, "-")}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

// 통계 업데이트
function updateStats() {
  const totalMsg = Object.values(conversations).reduce(
    (total, conv) => total + conv.messages.length,
    0
  );
  totalMessages.textContent = totalMsg;
  totalConversations.textContent = Object.keys(conversations).length;
}

// 스크롤 하단으로
function scrollToBottom() {
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

// API 호출 함수들
async function sendChatQuery(query, history=[]) {
  const response = await fetch('/api/chat/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, history })
  });
  return await response.json();
}

async function uploadImageAndGetModelCode(imageFile) {
  const formData = new FormData();
  formData.append("image", imageFile);

  const response = await fetch('/api/model-search/', {
    method: 'POST',
    body: formData
  });
  return await response.json();
}