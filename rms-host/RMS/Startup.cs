using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.OpenApi.Models;
using Npgsql;
using RMS.Handlers;
using RMS.services;
using RMS.services.Interfaces;

namespace RMS
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            // Initialize settings
            SettingsService.ImageKitPrivateKey = Configuration.GetSection("ImageKit").GetValue<string>("PrivateKey");
            SettingsService.ImageKitPublicKey = Configuration.GetSection("ImageKit").GetValue<string>("PublicKey");
            SettingsService.ImageKitURLEndpoint = Configuration.GetSection("ImageKit").GetValue<string>("URLEndpoint");
            SettingsService.EmailAddress = Configuration.GetSection("Email").GetValue<string>("Address");
            SettingsService.EmailPassword = Configuration.GetSection("Email").GetValue<string>("Password");
            
            // Initialize all of the controllers
            services.AddControllers();

            // Initialize database
            var builder = new NpgsqlConnectionStringBuilder
            {
                Host = "ec2-176-34-211-0.eu-west-1.compute.amazonaws.com",
                Port = 5432,
                Username = "gqwwuljwehotjx",
                Password = "ff5fb70ab39e6ec706b100a0d10f1adb43f48d4b52882833383115bacf14968a",
                Database = "d5rs3218pcv6mt",
                SslMode = SslMode.Require,
                TrustServerCertificate = true
            };
            
            services.AddDbContext<DbContext>(
                options => options.UseNpgsql(builder.ConnectionString));
            
            // Initialize authentication
            services.AddAuthentication("BasicAuthentication")
                .AddScheme<AuthenticationSchemeOptions, BasicAuthenticationHandler>("BasicAuthentication", null);
            
            // Custom services
            services.AddScoped<IImageService, ImageService>();
            services.AddScoped<IMemoryCache, MemoryCache>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            
            app.UseCors (x => x
                .AllowAnyOrigin ()
                .AllowAnyMethod ()
                .AllowAnyHeader ());

            app.UseHttpsRedirection();

            app.UseRouting();

            app.UseAuthentication();
            
            app.UseAuthorization();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}