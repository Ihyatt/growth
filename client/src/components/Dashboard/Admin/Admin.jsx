import { useState, useEffect } from 'react';
import { fetchUsers } from '../../../services/admin';
import { USER_STATUS, USER_ROLES } from '../../../utils/constants';
import User from './AdminContent/User';
import Pagination from './AdminContent/Pagination';


const Admin = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState({
    role: USER_ROLES.PRACTITIONER,
    status: USER_STATUS.PENDING,
    search: ''
  });
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    hasMore: true
  });

  const [queryParams, setQueryParams] = useState({
    status: USER_STATUS.PENDING,
    role: USER_ROLES.PRACTITIONER,
    limit: 10
  });

  const fetchUsers = async (reset = false) => {
    setLoading(true);
    try {
      const params = {
        ...query,
        page: reset ? 1 : pagination.page,
        limit: pagination.limit
      };
      
      const response = await axios.get('/api/users', { params });
      const newUsers = response.data.users;
      
      setUsers(prev => reset ? newUsers : [...prev, ...newUsers]);
      setPagination(prev => ({
        ...prev,
        page: reset ? 2 : prev.page + 1,
        hasMore: response.data.hasMore
      }));
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchUsers(true); // Reset pagination on new query
  };

  const handleLoadMore = () => {
    fetchUsers();
  };

  return (
    <div className="user-query">
      <form onSubmit={handleSubmit}>

     
        <select name="status" value={queryParams.status} >
          {Object.values(USER_STATUS).map(status => (
            <option key={status} value={status}>
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </option>
          ))}
        </select>
        
        <select name="role" value={queryParams.role} >
          {Object.values(USER_ROLES).map(role => (
            <option key={role} value={role}>
              {role.charAt(0).toUpperCase() + role.slice(1)}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Search by name"
          value={query.search}
          onChange={(e) => setQuery({...query, search: e.target.value})}
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      <div className="user-list">
        {users.map(user => (
          <div key={user.id} className="user-card">
            <h3>{user.name}</h3>
            <p>Role: {user.role}</p>
            <p>Status: {user.status}</p>
          </div>
        ))}
      </div>

      {pagination.hasMore && (
        <button 
          onClick={handleLoadMore} 
          disabled={loading}
          className="load-more"
        >
          {loading ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
};

export default Admin;