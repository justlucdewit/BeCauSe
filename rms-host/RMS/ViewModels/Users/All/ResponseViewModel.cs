using System;

namespace RMS.ViewModels.Users.All
{
    public class ResponseViewModel
    {
        public int Id { get; set; }

        public string FirstName { get; set; }
        
        public string LastName { get; set; }

        public string Email { get; set; }

        public string Address { get; set; }
        
        public string ProfilePicture { get; set; }
    }
}