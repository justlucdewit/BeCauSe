using System;
using Microsoft.EntityFrameworkCore.Migrations;

namespace RMS.Migrations
{
    public partial class CompanyOrdersMigration : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<Guid>(
                name: "ForCompanyId",
                table: "Orders",
                type: "uniqueidentifier",
                nullable: false,
                defaultValue: new Guid("00000000-0000-0000-0000-000000000000"));

            migrationBuilder.CreateIndex(
                name: "IX_Orders_ForCompanyId",
                table: "Orders",
                column: "ForCompanyId");

            migrationBuilder.AddForeignKey(
                name: "FK_Orders_Companies_ForCompanyId",
                table: "Orders",
                column: "ForCompanyId",
                principalTable: "Companies",
                principalColumn: "Id");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Orders_Companies_ForCompanyId",
                table: "Orders");

            migrationBuilder.DropIndex(
                name: "IX_Orders_ForCompanyId",
                table: "Orders");

            migrationBuilder.DropColumn(
                name: "ForCompanyId",
                table: "Orders");
        }
    }
}
