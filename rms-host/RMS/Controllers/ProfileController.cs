using System;
using System.Security.Cryptography;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Cryptography.KeyDerivation;
using Microsoft.AspNetCore.Mvc;
using RMS.Extensions;
using RMS.Helpers;
using RMS.services;
using RMS.services.Interfaces;

namespace RMS.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class ProfileController : BaseController
    {
        public ProfileController(DbContext databaseContext, IImageService imageService)
            : base(databaseContext, imageService)
        {
        }

        [Route("credentials")]
        [HttpPost]
        public async Task<IActionResult> UpdateCredentials([FromBody] ViewModels.Profile.UpdateCredentials.RequestViewModel request)
        {
            var currentUser = await getCurrentUser();
            
            string validationResult;
            
            // Validate username
            validationResult = await Validators.ValidateUsername(DbContext, request.UserName, currentUser.Id);
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

            currentUser.PasswordHash = hashed;
            currentUser.UserName = request.UserName;
            currentUser.PasswordSalt = Convert.ToHexString(salt);

            await DbContext.SaveChangesAsync();

            return Ok();
        }
        
        [Route("info")]
        [HttpPost]
        public async Task UpdateProfileInfo([FromBody] ViewModels.Profile.UpdateProfileInfo.RequestViewModel request)
        {
            var currentUser = await getCurrentUser();

            currentUser.FirstName = request.FirstName;
            currentUser.LastName = request.LastName;
            currentUser.Email = request.Email;
            currentUser.Address = request.Address;
            
            // If profile pic already set, remove it
            if (!currentUser.ProfilePicture.IsNullOrEmpty())
                await _imageService.DeleteImageURL(currentUser.ProfilePicture);

            string fileId = null;
            
            // Re upload the new profile picture, and get file Id
            if (!request.ProfilePicture.IsNullOrEmpty())
                fileId = await _imageService.UploadDataURI(
                    request.ProfilePicture,
                    "pfp_" + currentUser.Id);
            
            // Save the file Id
            currentUser.ProfilePicture = fileId;
            
            // Save changes to database
            await DbContext.SaveChangesAsync();
        }
    }
}