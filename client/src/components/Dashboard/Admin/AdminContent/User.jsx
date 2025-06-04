import React from 'react';
import { USER_STATUS, USER_ROLES } from '../../../../utils/constants';



export default function UserTable({ users=[], onRefresh }) {
    const handleAction = async (userId, action) => {
      // Implement approve/reject actions here
      console.log(`${action} user ${userId}`);
      // After action, refresh the list
      onRefresh();
    };
  
    return (
      <table className="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>
                <span className={`status-badge ${user.status}`}>
                  {user.status}
                </span>
              </td>
              <td className="actions">
                <button className="btn view">View</button>
                {user.status === USER_STATUS.PENDING && (
                  <>
                    <button 
                      className="btn approve"
                      onClick={() => handleAction(user.id, 'approve')}
                    >
                      Approve
                    </button>
                    <button 
                      className="btn reject"
                      onClick={() => handleAction(user.id, 'reject')}
                    >
                      Reject
                    </button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }