import { useState, useEffect } from 'react';
import { fetchUsers } from '../../../services/admin';
import useAuthStore from '../../../stores/auth';

import { USER_STATUS, USER_ROLES, USER_ACTIVE } from '../../../utils/constants';


const Admin = () => {
  const { jwtToken } = useAuthStore();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState({
    status: USER_STATUS.PENDING,
    role: USER_ROLES.PRACTITIONER,
    active: USER_ACTIVE.ACTIVE,
    email: '',
    limit: 10
  });
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    hasMore: true
  });

  const getUsers = async (reset = false) => {
    setLoading(true);
    try {
      const params = {
        ...query,
        page: reset ? 1 : pagination.page,
        limit: pagination.limit,
      };
      console.log(query)
      const response = await fetchUsers(params,jwtToken);
      const data = await response.json(); 
      const newUsers = data.users;
      console.log(users)
      
      setUsers(prev => reset ? newUsers : [...prev, ...newUsers]);
      setPagination(prev => ({
        ...prev,
        page: reset ? 2 : prev.page + 1,
        hasMore: data.hasMore
      }));
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    getUsers(true); // Reset pagination on new query
  };

  const handleLoadMore = () => {
    getUsers();
  };

  return (
    <div className="user-query">
      <form onSubmit={handleSubmit}>

     
        <select 
        name="status" 
        value={query.status} 
        onChange={(e) => setQuery({...query, status: e.target.value})}
        >
          {Object.values(USER_STATUS).map(status => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>

        <select 
        name="active" 
        value={query.active} 
        onChange={(e) => setQuery({...query, active: e.target.value})}
        >
        {Object.values(USER_ACTIVE).map(active => (
          <option key={active} value={active}>
            {active}
          </option>
        ))}
      </select>        
        <select 
        name="role" 
        value={query.role} 
        onChange={(e) => setQuery({...query, role: e.target.value})}
        >
          {Object.values(USER_ROLES).map(role => (
            <option key={role} value={role}>
              {role}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Search by email"
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
            <p>email: {user.email}</p>
            <p>Role: {user.permission}</p>
            <p>Validation Status: {user.is_validated}</p>
            <p>Activity Status: {user.is_active}</p>
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