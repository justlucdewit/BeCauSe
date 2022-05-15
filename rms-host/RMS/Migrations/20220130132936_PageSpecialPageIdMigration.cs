using Microsoft.EntityFrameworkCore.Migrations;

namespace RMS.Migrations
{
    public partial class PageSpecialPageIdMigration : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "SpecialPageId",
                table: "Pages",
                type: "nvarchar(max)",
                nullable: true);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "SpecialPageId",
                table: "Pages");
        }
    }
}
