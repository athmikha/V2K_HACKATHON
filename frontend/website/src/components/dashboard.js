import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Dashboard.css';
import{Link, Outlet} from 'react-router-dom';

function Dashboard() {
  const [data, setData] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/business/data');
        setData(response.data);
      } catch (error) {
        if (error.response) {
          setError(error.response.data.message);
        } else {
          setError('An error occurred. Please try again.');
        }
      }
    };

    fetchData();
  }, []);

  return (
    <div className="dashboard">
      <div className="sidebar">
        <h2>Sidebar</h2>
        <ul>
          <li><Link to="/Dashboard/signin"><button>Generate Bill</button></Link></li>
          <li><Link to="/signin"><button>Generate Bill</button></Link></li>
          <li><Link to="/signin"><button>Generate Bill</button></Link></li>
        </ul>
      </div>
      <div className="main-content">
        <h1>Dashboard</h1>
        {error && <p className="error">{error}</p>}
        <div className="data-container">
          {data.map((item, index) => (
            <div key={index} className="data-item">
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </div>
          ))}
           
        </div>
        <div className="dashcontent">
                    <div id="dashmain">
                        <Outlet />
        </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
