
import './App.css';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import SignIn from './components/signin';
import SignUp from './components/signup';
import Dashboard from './components/dashboard';
function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<SignIn />}/>
        <Route path='/signin' element={<SignIn />}/>
        <Route path='/signup' element={<SignUp />}/>
        <Route path='/dashboard' element={<Dashboard />}/>
        </Routes>
    </Router> 
  );
}

export default App;