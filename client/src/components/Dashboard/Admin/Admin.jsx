import { useState, useEffect } from 'react';
import { fetchUsers } from '../../../services/admin';
import { USER_STATUS, USER_ROLES } from '../../../utils/constants';
import User from './AdminContent/User';
import Pagination from './AdminContent/Pagination';

const Admin = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    nextCursor: null,
    prevCursor: null,
  });
  const [queryParams, setQueryParams] = useState({
    status: USER_STATUS.PENDING,
    role: USER_ROLES.PRACTITIONER,
    limit: 10
  });

  const loadUsers = async (cursor = null) => {
    setLoading(true);
    setError(null);
    
    try {
      const params = { ...queryParams, cursor };
      const data = await fetchUsers(params);
      console.log(data)

      setUsers(data.users);
      setPagination({
        nextCursor: data.has_next,
        prevCursor: data.has_prev,
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }

    console.log(users)
  };

  useEffect(() => {
    loadUsers();
  }, [queryParams]);

  const handleQueryChange = (e) => {
    const { name, value } = e.target;
    setQueryParams(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      
      <div className="filters">
        <select name="status" value={queryParams.status} onChange={handleQueryChange}>
          {Object.values(USER_STATUS).map(status => (
            <option key={status} value={status}>
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </option>
          ))}
        </select>
        
        <select name="role" value={queryParams.role} onChange={handleQueryChange}>
          {Object.values(USER_ROLES).map(role => (
            <option key={role} value={role}>
              {role.charAt(0).toUpperCase() + role.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">{error}</div>}

      <User users={users} onRefresh={loadUsers} />
      
      <Pagination 
        pagination={pagination}
        onNext={() => loadUsers(pagination.nextCursor)}
        onPrev={() => loadUsers(pagination.prevCursor)}
      />
    </div>
  );
}



export default Admin;