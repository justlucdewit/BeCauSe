using Microsoft.EntityFrameworkCore;
using RMS.Models;

namespace RMS
{
    public class DbContext : Microsoft.EntityFrameworkCore.DbContext
    {
        public DbContext(DbContextOptions<DbContext> options)
            : base(options)
        {
        }
        
        public DbSet<Company> Companies { get; set; }
        
        public DbSet<User> Users { get; set; }

        public DbSet<Product> Products { get; set; }

        public DbSet<Page> Pages { get; set; }

        public DbSet<CompanyModule> CompanyModules { get; set; }
        
        public DbSet<Order> Orders { get; set; }
        
        public DbSet<OrderItemSettings> OrderItemSettings { get; set; }
        
        public DbSet<CustomerDetails> CustomerDetails { get; set; }
        
        public DbSet<OrderItem> OrderItems { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Initialize tables
            modelBuilder.Entity<Company>().ToTable("Companies");
            modelBuilder.Entity<User>().ToTable("Users");
            modelBuilder.Entity<Product>().ToTable("Products");
            modelBuilder.Entity<Page>().ToTable("Pages");
            modelBuilder.Entity<CompanyModule>().ToTable("CompanyModules");
            modelBuilder.Entity<OrderItem>().ToTable("OrderItems");
            modelBuilder.Entity<Order>().ToTable("Orders");
            modelBuilder.Entity<OrderItemSettings>().ToTable("OrderItemSettings");
            modelBuilder.Entity<CustomerDetails>().ToTable("CustomerDetails");

            // Initialize database relations
            modelBuilder.Entity<Company>()
                .HasMany(company => company.Users)
                .WithOne(user => user.Company)
                .HasForeignKey(user => user.CompanyId)
                .OnDelete(DeleteBehavior.NoAction);

            modelBuilder.Entity<Company>()
                .HasMany(company => company.Products)
                .WithOne(product => product.Company)
                .HasForeignKey(product => product.CompanyId)
                .OnDelete(DeleteBehavior.NoAction);

            modelBuilder.Entity<Company>()
                .HasMany(company => company.Pages)
                .WithOne(product => product.Company)
                .HasForeignKey(product => product.CompanyId)
                .OnDelete(DeleteBehavior.NoAction);
            
            modelBuilder.Entity<Company>()
                .HasMany(company => company.CompanyModules)
                .WithOne(companyModule => companyModule.Company)
                .HasForeignKey(companyModule => companyModule.CompanyId)
                .OnDelete(DeleteBehavior.NoAction);

            modelBuilder.Entity<Product>()
                .HasMany(product => product.Orders)
                .WithOne(orderItem => orderItem.Product)
                .HasForeignKey(orderItem => orderItem.ProductId)
                .OnDelete(DeleteBehavior.NoAction);
            
            modelBuilder.Entity<Order>()
                .HasMany(order => order.Items)
                .WithOne(item => item.Order)
                .HasForeignKey(item => item.OrderId)
                .OnDelete(DeleteBehavior.NoAction);
            
            modelBuilder.Entity<OrderItem>()
                .HasMany(orderItem => orderItem.Settings)
                .WithOne(setting => setting.Item)
                .HasForeignKey(setting => setting.OrderItemId)
                .OnDelete(DeleteBehavior.NoAction);
            
            modelBuilder.Entity<Order>()
                .HasMany(order => order.Items)
                .WithOne(item => item.Order)
                .HasForeignKey(item => item.OrderId)
                .OnDelete(DeleteBehavior.NoAction);
            
            modelBuilder.Entity<Order>()
                .HasMany(order => order.CustomerDetails)
                .WithOne(customerDetails => customerDetails.Order)
                .HasForeignKey(customerDetails => customerDetails.OrderId)
                .OnDelete(DeleteBehavior.NoAction);
            
            modelBuilder.Entity<Order>()
                .HasOne(order => order.ForCompany)
                .WithMany(customerDetails => customerDetails.CompanyOrders)
                .HasForeignKey(order => order.ForCompanyId)
                .OnDelete(DeleteBehavior.NoAction);
        }
    }
}