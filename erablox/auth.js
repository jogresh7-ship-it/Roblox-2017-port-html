import { initializeApp } from "https://www.gstatic.com/firebasejs/10.0.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.0.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.0.0/firebase-firestore.js";

// Твой персональный конфиг для проекта erablox0
const firebaseConfig = {
  apiKey: "AIzaSyDZAjauAbq0tsLh1EZtaUp8-O9wbZmX4A8",
  authDomain: "erablox0.firebaseapp.com",
  projectId: "erablox0",
  storageBucket: "erablox0.firebasestorage.app",
  messagingSenderId: "747146722972",
  appId: "1:747146722972:web:2643f95690cb76c3bfb759",
  measurementId: "G-W8831YDFQR"
};

// Запуск Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Экспорт модулей, чтобы они были доступны в index.html
export { auth, db };
