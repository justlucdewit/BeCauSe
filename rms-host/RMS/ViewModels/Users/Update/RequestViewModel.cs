using System;

namespace RMS.ViewModels.Users.Update
{
    public class RequestViewModel
    {
        public int? Id { get; set; }

        public string FirstName { get; set; }
        
        public string LastName { get; set; }

        public string Email { get; set; }

        public string Address { get; set; }

        public string ProfilePicture { get; set; }

        public string Username { get; set; }
        
        public string Password { get; set; }
    }
}