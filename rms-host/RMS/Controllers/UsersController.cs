using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Cryptography.KeyDerivation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMS.Enums;
using RMS.Extensions;
using RMS.Helpers;
using RMS.Models;
using RMS.services;
using RMS.services.Interfaces;

namespace RMS.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class UsersController : BaseController
    {
        public UsersController(DbContext databaseContext, IImageService imageService)
            : base(databaseContext, imageService)
        {
        }
        
        /// <summary>
        /// GET: api/users/all
        /// </summary>
        [HttpGet("all")]
        public async Task<List<ViewModels.Users.All.ResponseViewModel>> GetAllUsers()
        {
            // Get the current user
            var currentUser = await getCurrentUser();

            var isSuperAdmin = currentUser.Role == Role.SuperAdmin;
            
            // Get all users
            var responseViewModel = await DbContext.Users
                .Where(user => (isSuperAdmin || user.Role != Role.SuperAdmin))
                .Select(user => new ViewModels.Users.All.ResponseViewModel
                {
                    Id = user.Id,
                    FirstName = user.FirstName,
                    LastName = user.LastName,
                    Email = user.Email,
                    Address = user.Address,
                    ProfilePicture = user.ProfilePicture,
                }).ToListAsync();
            
            // Dereference the profile picture
            foreach (var user in responseViewModel)
                user.ProfilePicture = user.ProfilePicture.IsNullOrEmpty()
                    ? ""
                    : await _imageService.DownloadImageURL(user.ProfilePicture);
            
            return responseViewModel;
        }
        
        /// <summary>
        /// POST: api/users/update
        /// </summary>
        [HttpPost("update")]
        public async Task<ActionResult> Update([FromBody] ViewModels.Users.Update.RequestViewModel request)
        {
            // Get the current user
            var currentUser = await getCurrentUser();
            
            // Create new user
            if (request.Id == null)
            {
                string profilePictureResource = "";
                
                // Store profile picture if profile picture exists
                if (!request.ProfilePicture.IsNullOrEmpty())
                    profilePictureResource = await _imageService.UploadDataURI(request.ProfilePicture, "pfp");
                
                string validationResult;
                
                // Validate username
                validationResult = await Validators.ValidateUsername(DbContext, request.Username, request.Id);
                if (!validationResult.IsNullOrEmpty())
                    return BadRequest(new { message = validationResult });
                
                // Validate password
                validationResult = Validators.ValidatePassword(request.Password);
                if (!validationResult.IsNullOrEmpty())
                    return BadRequest(new { message = validationResult });

                // Generate a new password salt
                byte[] salt = new byte[128 / 8];
                using (var rngCsp = new RNGCryptoServiceProvider())
                    rngCsp.GetNonZeroBytes(salt);
            
                // Generate a new password hash
                string hashed = Convert.ToBase64String(KeyDerivation.Pbkdf2(
                    password: request.Password,
                    salt: salt,
                    prf: KeyDerivationPrf.HMACSHA256,
                    iterationCount: 100000,
                    numBytesRequested: 256 / 8));
                
                // Create and store the user
                await DbContext.Users.AddAsync(new User
                {
                    FirstName = request.FirstName,
                    LastName = request.LastName,
                    Email = request.Email,
                    Address = request.Address,
                    UserName = request.Username,
                    PasswordHash = hashed,
                    PasswordSalt = Convert.ToHexString(salt),
                    ProfilePicture = profilePictureResource,
                    Role = Role.Employee,
                    CompanyId = currentUser.CompanyId
                });
            }
            
            // Update existing user
            else
            {
                // Retrieve the user from the database
                var dbUser = await DbContext.Users.FirstOrDefaultAsync(user => user.Id == request.Id);
                
                if (dbUser == null)
                    return BadRequest(new { message = "Unable to update user because user does not exist" });
                
                // Update the simple values
                dbUser.FirstName = request.FirstName;
                dbUser.LastName = request.LastName;
                dbUser.Email = request.Email;
                dbUser.Address = request.Address;
                
                // Delete the old profile picture
                string fileId = null;
                
                if (!dbUser.ProfilePicture.IsNullOrEmpty())
                    await _imageService.DeleteImageURL(dbUser.ProfilePicture);
                
                if (!request.ProfilePicture.IsNullOrEmpty())
                    fileId = await _imageService.UploadDataURI(
                        request.ProfilePicture,
                        "pfp_" + dbUser.Id);
                
                dbUser.ProfilePicture = fileId;

                if (request.Username != null && request.Password != null)
                {
                    string validationResult;
                    
                    // Validate username
                    validationResult = await Validators.ValidateUsername(DbContext, request.Username, request.Id);
                    if (!validationResult.IsNullOrEmpty())
                        return BadRequest(new { message = validationResult });
                    
                    // Validate password
                    validationResult = Validators.ValidatePassword(request.Password);
                    if (!validationResult.IsNullOrEmpty())
                        return BadRequest(new { message = validationResult });
                    
                    // Generate a new password salt
                    byte[] salt = new byte[128 / 8];
                    using (var rngCsp = new RNGCryptoServiceProvider())
                        rngCsp.GetNonZeroBytes(salt);
            
                    // Generate a new password hash
                    string hashed = Convert.ToBase64String(KeyDerivation.Pbkdf2(
                        password: request.Password,
                        salt: salt,
                        prf: KeyDerivationPrf.HMACSHA256,
                        iterationCount: 100000,
                        numBytesRequested: 256 / 8));

                    dbUser.UserName = request.Username;
                    dbUser.PasswordHash = hashed;
                    dbUser.PasswordSalt = Convert.ToHexString(salt);
                }
            }
            
            // Save the changes to the database
            await DbContext.SaveChangesAsync();

            return Ok();
        }
        
        /// <summary>
        /// DELETE: api/users/delete/{userId}
        /// </summary>
        [HttpPost("delete/{userId:int}")]
        public async Task<ActionResult> Delete([FromRoute] int userId)
        {
            var dbUser = await DbContext.Users.FirstOrDefaultAsync(dbUser => dbUser.Id == userId);

            if (dbUser == null)
                return BadRequest(new { message = "Unable to delete user because user does not exist" });
            
            // Delete the profile image if exists
            if (!dbUser.ProfilePicture.IsNullOrEmpty())
                await _imageService.DeleteImageURL(dbUser.ProfilePicture);
            
            DbContext.Users.Remove(dbUser);
            
            await DbContext.SaveChangesAsync();
            
            return Ok();
        }
    }
}