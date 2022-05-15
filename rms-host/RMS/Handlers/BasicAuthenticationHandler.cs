using System;
using System.Linq;
using System.Net.Http.Headers;
using System.Security.Claims;
using System.Text;
using System.Text.Encodings.Web;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Cryptography.KeyDerivation;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace RMS.Handlers
{
    public class BasicAuthenticationHandler : AuthenticationHandler<AuthenticationSchemeOptions>
    {
        private static DbContext _dbContext;
        
        public BasicAuthenticationHandler(
            IOptionsMonitor<AuthenticationSchemeOptions> options,
            ILoggerFactory logger,
            UrlEncoder encoder,
            ISystemClock clock,
            DbContext dbContext)
             : base(options, logger, encoder, clock)
             {
                 _dbContext = dbContext;
             }

        protected override async Task<AuthenticateResult> HandleAuthenticateAsync()
        {
            if (!Request.Headers.ContainsKey("Authorization"))
                return AuthenticateResult.Fail("Authorization header was missing");

            var authenticationHeaderValue = AuthenticationHeaderValue.Parse(Request.Headers["Authorization"]);

            var bytes = Convert.FromBase64String(authenticationHeaderValue.Parameter);

            var credentials = Encoding.UTF8.GetString(bytes).Split(":");
            
            if (credentials.Length != 2)
                return AuthenticateResult.Fail("Authorization format was flawed");
            
            string username = credentials[0];
            string password = credentials[1];

            var dbUser = _dbContext.Users.FirstOrDefault(user => user.UserName == username);
            
            if (dbUser == null)
                return AuthenticateResult.Fail("Username or password was incorrect");
            
            string passwordHash = Convert.ToBase64String(KeyDerivation.Pbkdf2(
                password: password,
                salt: Convert.FromHexString(dbUser.PasswordSalt),
                prf: KeyDerivationPrf.HMACSHA256,
                iterationCount: 100000,
                numBytesRequested: 256 / 8));

            if (passwordHash != dbUser.PasswordHash)
            {
                return AuthenticateResult.Fail("Username or password was incorrect");
            }
            else
            {
                var claims = new[]
                {
                    new Claim(ClaimTypes.PrimarySid, dbUser.Id.ToString())
                };
                var identity = new ClaimsIdentity(claims, Scheme.Name);
                var principal = new ClaimsPrincipal(identity);
                var ticket = new AuthenticationTicket(principal, Scheme.Name);
                
                return AuthenticateResult.Success(ticket);
            }
        }
    }
}