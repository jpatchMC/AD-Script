###this is to look up the vault so wrong
data "azurerm_key_vault" "example" {
  name                = "mykeyvault"
  resource_group_name = "some-resource-group"
}

output "vault_uri" {
  value = data.azurerm_key_vault.example.vault_uri
}
###this one is correct
data "azurerm_key_vault_secret" "example" {
  name         = "secret-sauce"
  key_vault_id = data.azurerm_key_vault.existing.id
}

output "secret_value" {
  value     = data.azurerm_key_vault_secret.example.value
  sensitive = true
}