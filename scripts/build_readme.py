#!/usr/bin/env python3
import json
import os
import sys

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root_dir, "promo.json")
    template_path = os.path.join(root_dir, "README.template.md")
    output_path = os.path.join(root_dir, "README.md")

    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        sys.exit(1)

    if not os.path.exists(template_path):
        print(f"Error: {template_path} not found.")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    updated_date = config.get("updated_date", "")
    updated_date_header = f" (Updated {updated_date})" if updated_date else ""

    is_promo = config.get("is_promo_active", False)
    promo_banner = config.get("promo_banner_text", "").strip()
    active_promo_banner = f"{promo_banner}\n\n" if (is_promo and promo_banner) else ""

    default_discount = config.get("default_discount", "30% OFF")
    default_code = config.get("default_code", "30K8SUG")
    section_discounts = config.get("section_discounts", {})
    overrides = config.get("overrides", {})

    replacements = {
        "{{UPDATED_DATE_HEADER}}": updated_date_header,
        "{{ACTIVE_PROMO_BANNER}}": active_promo_banner,
    }

    # Section Headers
    for sec_key, sec_name in [
        ("kubestronaut", "KUBESTRONAUT"),
        ("bundles", "BUNDLE"),
        ("individual", "INDIVIDUAL"),
    ]:
        sec_disc = section_discounts.get(sec_key, default_discount)
        replacements[f"{{{{{sec_name}_SECTION_DISCOUNT}}}}"] = sec_disc
        if default_code:
            replacements[f"{{{{{sec_name}_SECTION_CODE_TEXT}}}}"] = f" • Code: `{default_code}`"
        else:
            replacements[f"{{{{{sec_name}_SECTION_CODE_TEXT}}}}"] = ""

    # Items
    items = [
        "CYBER", "CLOUD", "DEV",
        "KB", "GK", "KGU", "CKAU", "CKADU",
        "SACKS", "NASA", "CKAAD", "CKAS", "NACKA", "CKADS", "ICA", "CAPA", "LFCA_KCNA", "LFCA_LFS200", "PCA_BUNDLE",
        "CKA", "CKAD", "CKS", "KCNA", "KCSA", "PCA", "ICA_CERT", "CAPA_CERT", "CGOA", "CCA", "CBA", "OTCA", "KCA", "LFCS", "CNPA", "CNPE"
    ]

    for item in items:
        item_override = overrides.get(item, {})
        disc = item_override.get("discount", default_discount)
        code = item_override.get("code", default_code)

        replacements[f"{{{{{item}_DISCOUNT}}}}"] = disc
        replacements[f"{{{{{item}_CODE}}}}"] = code

    rendered = template
    for key, val in replacements.items():
        rendered = rendered.replace(key, val)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    main()
