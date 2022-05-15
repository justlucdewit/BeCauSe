using System;
using System.Collections.Generic;
using RMS.Enums;

namespace RMS.Models
{
    public class User
    {
        public int Id { get; set; }

        public string FirstName { get; set; }

        public string LastName { get; set; }

        public string Email { get; set; }

        public string Address { get; set; }

        public string UserName { get; set; }

        public string PasswordHash { get; set; }

        public string PasswordSalt { get; set; }

        public string ProfilePicture { get; set; }

        public Role Role { get; set; }

        public int CompanyId { get; set; }

        public virtual Company Company { get; set; }
    }
}