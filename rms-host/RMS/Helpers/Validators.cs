using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using RMS.Extensions;

namespace RMS.Helpers
{
    public static class Validators
    {
        public static string ValidatePassword(string password)
        {
            // Validate password is not null
            if (password == null)
                return "Password cannot be empty";
            
            // Validate password length
            if (password.Length < 8 || password.Length > 128)
                return "Password must be between 8 and 128 characters";
            
            // Validate password uppercase letter
            if (!password.Any(character => "ABCDEFGHIJKLMNOPQRSTUVWXYZ".Contains(character)))
                return "Password must contain at least one uppercase letter";
            
            // Validate password characters
            if (!password.ContainsOnlyAllowedChars("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-!@%#$&*"))
                return "Password may only contain a-z, A-Z, 0-9 and special characters (_.-!@%#$&*)";

            return null;
        }

        public static async Task<string> ValidateUsername(DbContext DbContext, string username, int? currentUserId)
        {
            // Validate if the username is empty
            if (username == null)
                return "Username cannot be empty";

            // Validate if username already exist (but ignore current user)
            if (await DbContext.Users.AnyAsync(user => user.UserName == username && user.Id != currentUserId))
                return "Username is already taken";
            
            // Validate username length
            if (username.Length > 30 || username.Length < 6)
                return "Username must be between 6 and 30 characters";
            
            // Validate username characters
            if (!username.ContainsOnlyAllowedChars("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-"))
                return "Username may only contain a-z, A-Z, 0-9, underscores (_), dots (.) and dashes (-)";
            
            return null;
        }
    }
}