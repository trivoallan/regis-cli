from regis_cli.playbook.engine import evaluate, load_playbook

pb = load_playbook("regis_cli/playbooks/default.yaml")
print("LOADED PLAYBOOK:")
pages = pb.get("pages", [])
for p in pages:
    if p.get("slug") == "security":
        print(p)

res = evaluate(pb, {"results": {}})
for p in res.get("pages", []):
    if p.get("slug") == "security":
        print("EVALUATED PAGE:")
        print(p)
