import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './index.css';
import App from './App';
import AboutPage from './pages/AboutPage/AboutPage';
import UploadPage from './pages/UploadPage/UploadPage';
import SettingPage from './pages/SettingPage/SettingPage';
import HomePage from './pages/HomePage/HomePage';
import EditImagePage from './pages/EditImagePage/EditImagePage';
import ImageGenPage from './pages/ImageGenPage/ImageGenPage';
import TermsPage from './pages/TermsPage/TermsPage';
import LoginPage from './pages/LoginPage/LoginPage';
import CaptionGenPage from './pages/CaptionGenPage/CaptionGenPage';
import SignUpPage from './pages/SignUpPage/SignUpPage';

import ArchivePage from './pages/ArchivePage/ArchivePage';

import NavBar from './components/NavBar/NavBar';

// import HomePage from './pages/HomePage/HomePage';
import NotFoundPage from './pages//NotFoundPage/NotFoundPage';
import reportWebVitals from './reportWebVitals';
import ExplorePage from './pages/ExplorePage/ExplorePage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <NavBar/>
    <ToastContainer />
    <Router>
      <Routes>
        <Route path="/" exact element={<HomePage/>} />
        {/* <Route path="/home" exact element={<HomePage/>} /> */}
        <Route path="/About" element={<AboutPage/>} />
        {/* CaptionGen */}
        <Route path="/Explore" element={<ExplorePage/>} />
        <Route path="/CaptionGen" element={<CaptionGenPage/>} />
        <Route path="/EditImage" element={<EditImagePage/>} />
        <Route path="/ImageGen" element={<ImageGenPage/>} />
        <Route path="/SignUp" element={<SignUpPage/>} />
        <Route path="/Login" element={<LoginPage/>} />
        <Route path="/Archive" element={<ArchivePage/>} />
        <Route path="/TermsandConditions" element={<TermsPage/>} />
        <Route path="/Setting" element={<SettingPage/>} />
        <Route path="*" exact={true} element={<NotFoundPage/>} />
      </Routes>
    </Router>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
