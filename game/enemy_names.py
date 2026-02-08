import random

enemy_names = {
    "Brasswick": 0, "Cogsworth": 0, "Steamweld": 0, "Gearlock": 0, "Ironwisp": 0,
    "Valvegrim": 0, "Rusthaven": 0, "Boltmarrow": 0, "Pistonshade": 0, "Copperthorn": 0,
    "Sprockett": 0, "Grimcog": 0, "Wrenchmaw": 0, "Boilsteam": 0, "Gasketbane": 0,
    "Ironquill": 0, "Brimgear": 0, "Steamjaw": 0, "Rustclank": 0, "Valvegrim": 0,
    "Furnacelash": 0, "Smokestitch": 0, "Gearshank": 0, "Coppergrim": 0, "Boltshroud": 0,
    "Pistongrim": 0, "Sootweld": 0, "Ironshank": 0, "Steamthorn": 0, "Rustspine": 0,
    "Cogshroud": 0, "Gearmaw": 0, "Brasslash": 0, "Valvewisp": 0, "Boltforge": 0,
    "Pistonclaw": 0, "Copperjaw": 0, "Sootfang": 0, "Ironlash": 0, "Steamclank": 0,
    "Rustjaw": 0, "Gearthorn": 0, "Cogmarrow": 0, "Brassclank": 0, "Valvefang": 0,
    "Boltweld": 0, "Pistonthorn": 0, "Copperclaw": 0, "Sootshank": 0, "Ironfang": 0,
    "Steamspine": 0, "Rustlash": 0, "Gearweld": 0, "Cogthorn": 0, "Brassmaw": 0,
    "Valveclaw": 0, "Boltwisp": 0, "Pistonforge": 0, "Copperweld": 0, "Sootclank": 0,
    "Ironweld": 0, "Steamfang": 0, "Rustforge": 0, "Gearlash": 0, "Cogfang": 0,
    "Brassforge": 0, "Valvejaw": 0, "Boltclank": 0, "Pistonsmoke": 0, "Coppersteam": 0,
    "Sootgear": 0, "Ironsteam": 0, "Steamgear": 0, "Rustgear": 0, "Gearsteam": 0,
    "Cogsteam": 0, "Brasssteam": 0, "Valvesteam": 0, "Boltsteam": 0, "Pistonsteam": 0,
    "Copperbolt": 0, "Sootbolt": 0, "Ironbolt": 0, "Steambolt": 0, "Rustbolt": 0,
    "Gearbolt": 0, "Cogbolt": 0, "Brassbolt": 0, "Valvebolt": 0, "Boltgear": 0,
    "Pistongear": 0, "Coppergear": 0, "Sootgear": 0, "Irongear": 0, "Steamclaw": 0,
    "Rustclaw": 0, "Gearclaw": 0, "Cogclaw": 0, "Brassclaw": 0, "Valveclaw": 0,
    "Boltclaw": 0, "Pistonclaw": 0, "Copperclaw": 0, "Sootclaw": 0, "Ironclaw": 0,
    "Steamweld": 0, "Rustweld": 0, "Gearweld": 0, "Cogweld": 0, "Brassweld": 0,
    "Valveweld": 0, "Boltweld": 0, "Pistonweld": 0, "Copperweld": 0, "Sootweld": 0,
    "Ironwisp": 0, "Steamwisp": 0, "Rustwisp": 0, "Gearwisp": 0, "Cogwisp": 0,
    "Brasswisp": 0, "Valvewisp": 0, "Boltwisp": 0, "Pistonwisp": 0, "Copperwisp": 0,
    "Sootwisp": 0, "Ironshroud": 0, "Steamshroud": 0, "Rustshroud": 0, "Gearshroud": 0,
    "Cogshroud": 0, "Brassshroud": 0, "Valveshroud": 0, "Boltshroud": 0, "Pistonshroud": 0,
    "Coppershroud": 0, "Sootshroud": 0, "Ironmarrow": 0, "Steammarrow": 0, "Rustmarrow": 0,
    "Gearmarrow": 0, "Cogmarrow": 0, "Brassmarrow": 0, "Valvemarrow": 0, "Boltmarrow": 0,
    "Pistonmarrow": 0, "Coppermarrow": 0, "Sootmarrow": 0
}
enemy_names.update({
    "Gearhaunt": 0, "Rustreaver": 0, "Steamgloom": 0, "Ironmire": 0, "Boltshank": 0,
    "Coppergrim": 0, "Valvebrand": 0, "Sootreign": 0, "Brassmire": 0, "Cogwrath": 0,
    "Gearshatter": 0, "Rustwrought": 0, "Steamreaver": 0, "Ironshackle": 0, "Boltgrind": 0,
    "Copperlash": 0, "Valvescour": 0, "Sootmonger": 0, "Brassgrind": 0, "Cogbreaker": 0,
    "Gearmonger": 0, "Rustfang": 0, "Steamshank": 0, "Ironshroud": 0, "Boltmaw": 0,
    "Coppermaw": 0, "Valvemauler": 0, "Sootshank": 0, "Brasslash": 0, "Coglash": 0,
    "Gearlash": 0, "Rustlash": 0, "Steamlash": 0, "Ironlash": 0, "Boltlash": 0,
    "Copperlash": 0, "Valvelash": 0, "Sootlash": 0, "Brasslash": 0, "Coglash": 0,
    "Geargrit": 0, "Rustgrit": 0, "Steamgrit": 0, "Irongrit": 0, "Boltgrit": 0,
    "Coppergrit": 0, "Valvegrit": 0, "Sootgrit": 0, "Brassgrit": 0, "Coggrit": 0,
    "Gearshank": 0, "Rustshank": 0, "Steamshank": 0, "Ironshank": 0, "Boltshank": 0,
    "Coppershank": 0, "Valveshank": 0, "Sootshank": 0, "Brassshank": 0, "Cogshank": 0,
    "Gearmauler": 0, "Rustmauler": 0, "Steammauler": 0, "Ironmauler": 0, "Boltmauler": 0,
    "Coppermauler": 0, "Valvemauler": 0, "Sootmauler": 0, "Brassmauler": 0, "Cogmauler": 0,
    "Gearmire": 0, "Rustmire": 0, "Steammire": 0, "Ironmire": 0, "Boltmire": 0,
    "Coppermire": 0, "Valvemire": 0, "Sootmire": 0, "Brassmire": 0, "Cogmire": 0,
    "Gearshroud": 0, "Rustshroud": 0, "Steamshroud": 0, "Ironshroud": 0, "Boltshroud": 0,
    "Coppershroud": 0, "Valveshroud": 0, "Sootshroud": 0, "Brassshroud": 0, "Cogshroud": 0,
    "Gearwrought": 0, "Rustwrought": 0, "Steamwrought": 0, "Ironwrought": 0, "Boltwrought": 0,
    "Copperwrought": 0, "Valvewrought": 0, "Sootwrought": 0, "Brasswrought": 0, "Cogwrought": 0,
    "Geargrim": 0, "Rustgrim": 0, "Steamgrim": 0, "Irongrim": 0, "Boltgrim": 0,
    "Coppergrim": 0, "Valvegrim": 0, "Sootgrim": 0, "Brassgrim": 0, "Coggrim": 0,
    "Gearbane": 0, "Rustbane": 0, "Steambane": 0, "Ironbane": 0, "Boltbane": 0,
    "Copperbane": 0, "Valvebane": 0, "Sootbane": 0, "Brassbane": 0, "Cogbane": 0,
    "Gearmourn": 0, "Rustmourn": 0, "Steammourn": 0, "Ironmourn": 0, "Boltmourn": 0,
    "Coppermourn": 0, "Valvemourn": 0, "Sootmourn": 0, "Brassmourn": 0, "Cogmourn": 0,
    "Gearreaver": 0, "Rustreaver": 0, "Steamreaver": 0, "Ironreaver": 0, "Boltreaver": 0,
    "Copperreaver": 0, "Valvereaver": 0, "Sootreaver": 0, "Brassreaver": 0, "Cogreaver": 0,
    "Gearhauler": 0, "Rusthauler": 0, "Steamhauler": 0, "Ironhauler": 0, "Bolthauler": 0,
    "Copperhauler": 0, "Valvehauler": 0, "Soothauler": 0, "Brasshauler": 0, "Coghauler": 0,
    "Gearmancer": 0, "Rustmancer": 0, "Steammancer": 0, "Ironmancer": 0, "Boltmancer": 0,
    "Coppermancer": 0, "Valvemancer": 0, "Sootmancer": 0, "Brassmancer": 0, "Cogmancer": 0,
    "Gearshiver": 0, "Rustshiver": 0, "Steamshiver": 0, "Ironshiver": 0, "Boltshiver": 0,
    "Coppershiver": 0, "Valveshiver": 0, "Sootshiver": 0, "Brassshiver": 0, "Cogshiver": 0,
    "Gearmolder": 0, "Rustmolder": 0, "Steammolder": 0, "Ironmolder": 0, "Boltmolder": 0,
    "Coppermolder": 0, "Valvemolder": 0, "Sootmolder": 0, "Brassmolder": 0, "Cogmolder": 0,
    "Gearshackle": 0, "Rustshackle": 0, "Steamshackle": 0, "Ironshackle": 0, "Boltshackle": 0,
    "Coppershackle": 0, "Valveshackle": 0, "Sootshackle": 0, "Brassshackle": 0, "Cogshackle": 0,
    "Gearmortar": 0, "Rustmortar": 0, "Steammortar": 0, "Ironmortar": 0, "Boltmortar": 0,
    "Coppermortar": 0, "Valvemortar": 0, "Sootmortar": 0, "Brassmortar": 0, "Cogmortar": 0,
    "Gearshatter": 0, "Rustshatter": 0, "Steamshatter": 0, "Ironshatter": 0, "Boltshatter": 0,
    "Coppershatter": 0, "Valveshatter": 0, "Sootshatter": 0, "Brassshatter": 0, "Cogshatter": 0,
    "Gearmireborn": 0, "Rustmireborn": 0, "Steammireborn": 0, "Ironmireborn": 0, "Boltmireborn": 0,
    "Coppermireborn": 0, "Valvemireborn": 0, "Sootmireborn": 0, "Brassmireborn": 0, "Cogmireborn": 0,
    "Gearhollow": 0, "Rusthollow": 0, "Steamhollow": 0, "Ironhollow": 0, "Bolthollow": 0,
    "Copperhollow": 0, "Valvehollow": 0, "Soothollow": 0, "Brasshollow": 0, "Coghollow": 0
})
enemy_names.update({
    "Gearspire": 0, "Rustspire": 0, "Steamspire": 0, "Ironspire": 0, "Boltspire": 0,
    "Copperspire": 0, "Valvespire": 0, "Sootspire": 0, "Brassspire": 0, "Cogspire": 0,
    "Gearhaze": 0, "Rusthaze": 0, "Steamhaze": 0, "Ironhaze": 0, "Bolthaze": 0,
    "Copperhaze": 0, "Valvehaze": 0, "Soothaze": 0, "Brasshaze": 0, "Coghaze": 0,
    "Gearveil": 0, "Rustveil": 0, "Steamveil": 0, "Ironveil": 0, "Boltveil": 0,
    "Copperveil": 0, "Valveveil": 0, "Sootveil": 0, "Brassveil": 0, "Cogveil": 0,
    "Gearshale": 0, "Rustshale": 0, "Steamshale": 0, "Ironshale": 0, "Boltshale": 0,
    "Coppershale": 0, "Valveshale": 0, "Sootshale": 0, "Brassshale": 0, "Cogshale": 0,
    "Gearblight": 0, "Rustblight": 0, "Steamblight": 0, "Ironblight": 0, "Boltblight": 0,
    "Copperblight": 0, "Valveblight": 0, "Sootblight": 0, "Brassblight": 0, "Cogblight": 0,
    "Gearmireborn": 0, "Rustmireborn": 0, "Steammireborn": 0, "Ironmireborn": 0, "Boltmireborn": 0,
    "Coppermireborn": 0, "Valvemireborn": 0, "Sootmireborn": 0, "Brassmireborn": 0, "Cogmireborn": 0,
    "Gearshorn": 0, "Rustshorn": 0, "Steamshorn": 0, "Ironshorn": 0, "Boltshorn": 0,
    "Coppershorn": 0, "Valveshorn": 0, "Sootshorn": 0, "Brassshorn": 0, "Cogshorn": 0,
    "Gearmold": 0, "Rustmold": 0, "Steammold": 0, "Ironmold": 0, "Boltmold": 0,
    "Coppermold": 0, "Valvemold": 0, "Sootmold": 0, "Brassmold": 0, "Cogmold": 0,
    "Gearshankborn": 0, "Rustshankborn": 0, "Steamshankborn": 0, "Ironshankborn": 0, "Boltshankborn": 0,
    "Coppershankborn": 0, "Valveshankborn": 0, "Sootshankborn": 0, "Brassshankborn": 0, "Cogshankborn": 0,
    "Gearhollowborn": 0, "Rusthollowborn": 0, "Steamhollowborn": 0, "Ironhollowborn": 0, "Bolthollowborn": 0,
    "Copperhollowborn": 0, "Valvehollowborn": 0, "Soothollowborn": 0, "Brasshollowborn": 0, "Coghollowborn": 0,
    "Gearshiverborn": 0, "Rustshiverborn": 0, "Steamshiverborn": 0, "Ironshiverborn": 0, "Boltshiverborn": 0,
    "Coppershiverborn": 0, "Valveshiverborn": 0, "Sootshiverborn": 0, "Brassshiverborn": 0, "Cogshiverborn": 0,
    "Geargrindborn": 0, "Rustgrindborn": 0, "Steamgrindborn": 0, "Irongrindborn": 0, "Boltgrindborn": 0,
    "Coppergrindborn": 0, "Valvegrindborn": 0, "Sootgrindborn": 0, "Brassgrindborn": 0, "Coggrindborn": 0,
    "Gearshatterborn": 0, "Rustshatterborn": 0, "Steamshatterborn": 0, "Ironshatterborn": 0, "Boltshatterborn": 0,
    "Coppershatterborn": 0, "Valveshatterborn": 0, "Sootshatterborn": 0, "Brassshatterborn": 0, "Cogshatterborn": 0,
    "Gearmournborn": 0, "Rustmournborn": 0, "Steammournborn": 0, "Ironmournborn": 0, "Boltmournborn": 0,
    "Coppermournborn": 0, "Valvemournborn": 0, "Sootmournborn": 0, "Brassmournborn": 0, "Cogmournborn": 0,
    "Gearhauntborn": 0, "Rusthauntborn": 0, "Steamhauntborn": 0, "Ironhauntborn": 0, "Bolthauntborn": 0,
    "Copperhauntborn": 0, "Valvehauntborn": 0, "Soothauntborn": 0, "Brasshauntborn": 0, "Coghauntborn": 0,
    "Gearshroudling": 0, "Rustshroudling": 0, "Steamshroudling": 0, "Ironshroudling": 0, "Boltshroudling": 0,
    "Coppershroudling": 0, "Valveshroudling": 0, "Sootshroudling": 0, "Brassshroudling": 0, "Cogshroudling": 0,
    "Gearmireling": 0, "Rustmireling": 0, "Steammireling": 0, "Ironmireling": 0, "Boltmireling": 0,
    "Coppermireling": 0, "Valvemireling": 0, "Sootmireling": 0, "Brassmireling": 0, "Cogmireling": 0,
    "Geargritling": 0, "Rustgritling": 0, "Steamgritling": 0, "Irongritling": 0, "Boltgritling": 0,
    "Coppergritling": 0, "Valvegritling": 0, "Sootgritling": 0, "Brassgritling": 0, "Coggritling": 0,
    "Gearshankling": 0, "Rustshankling": 0, "Steamshankling": 0, "Ironshankling": 0, "Boltshankling": 0,
    "Coppershankling": 0, "Valveshankling": 0, "Sootshankling": 0, "Brassshankling": 0, "Cogshankling": 0,
    "Gearweldling": 0, "Rustweldling": 0, "Steamweldling": 0, "Ironweldling": 0, "Boltweldling": 0,
    "Copperweldling": 0, "Valveweldling": 0, "Sootweldling": 0, "Brassweldling": 0, "Cogweldling": 0,
    "Gearclankling": 0, "Rustclankling": 0, "Steamclankling": 0, "Ironclankling": 0, "Boltclankling": 0,
    "Copperclankling": 0, "Valveclankling": 0, "Sootclankling": 0, "Brassclankling": 0, "Cogclankling": 0
})
enemy_names.update({
    "Gearflare": 0, "Rustflare": 0, "Steamflare": 0, "Ironflare": 0, "Boltflare": 0,
    "Copperflare": 0, "Valveflare": 0, "Sootflare": 0, "Brassflare": 0, "Cogflare": 0,
    "Gearhollowshade": 0, "Rusthollowshade": 0, "Steamhollowshade": 0, "Ironhollowshade": 0, "Bolthollowshade": 0,
    "Copperhollowshade": 0, "Valvehollowshade": 0, "Soothollowshade": 0, "Brasshollowshade": 0, "Coghollowshade": 0,
    "Gearshattergeist": 0, "Rustshattergeist": 0, "Steamshattergeist": 0, "Ironshattergeist": 0, "Boltshattergeist": 0,
    "Coppershattergeist": 0, "Valveshattergeist": 0, "Sootshattergeist": 0, "Brassshattergeist": 0, "Cogshattergeist": 0,
    "Gearmourngeist": 0, "Rustmourngeist": 0, "Steammourngeist": 0, "Ironmourngeist": 0, "Boltmourngeist": 0,
    "Coppermourngeist": 0, "Valvemourngeist": 0, "Sootmourngeist": 0, "Brassmourngeist": 0, "Cogmourngeist": 0,
    "Geargrindgeist": 0, "Rustgrindgeist": 0, "Steamgrindgeist": 0, "Irongrindgeist": 0, "Boltgrindgeist": 0,
    "Coppergrindgeist": 0, "Valvegrindgeist": 0, "Sootgrindgeist": 0, "Brassgrindgeist": 0, "Coggrindgeist": 0,
    "Gearshankgeist": 0, "Rustshankgeist": 0, "Steamshankgeist": 0, "Ironshankgeist": 0, "Boltshankgeist": 0,
    "Coppershankgeist": 0, "Valveshankgeist": 0, "Sootshankgeist": 0, "Brassshankgeist": 0, "Cogshankgeist": 0,
    "Gearweldgeist": 0, "Rustweldgeist": 0, "Steamweldgeist": 0, "Ironweldgeist": 0, "Boltweldgeist": 0,
    "Copperweldgeist": 0, "Valveweldgeist": 0, "Sootweldgeist": 0, "Brassweldgeist": 0, "Cogweldgeist": 0,
    "Gearclankgeist": 0, "Rustclankgeist": 0, "Steamclankgeist": 0, "Ironclankgeist": 0, "Boltclankgeist": 0,
    "Copperclankgeist": 0, "Valveclankgeist": 0, "Sootclankgeist": 0, "Brassclankgeist": 0, "Cogclankgeist": 0,
    "Gearhazegeist": 0, "Rusthazegeist": 0, "Steamhazegeist": 0, "Ironhazegeist": 0, "Bolthazegeist": 0,
    "Copperhazegeist": 0, "Valvehazegeist": 0, "Soothazegeist": 0, "Brasshazegeist": 0, "Coghazegeist": 0,
    "Gearveilgeist": 0, "Rustveilgeist": 0, "Steamveilgeist": 0, "Ironveilgeist": 0, "Boltveilgeist": 0,
    "Copperveilgeist": 0, "Valveveilgeist": 0, "Sootveilgeist": 0, "Brassveilgeist": 0, "Cogveilgeist": 0,
    "Gearblightgeist": 0, "Rustblightgeist": 0, "Steamblightgeist": 0, "Ironblightgeist": 0, "Boltblightgeist": 0,
    "Copperblightgeist": 0, "Valveblightgeist": 0, "Sootblightgeist": 0, "Brassblightgeist": 0, "Cogblightgeist": 0,
    "Gearflareborn": 0, "Rustflareborn": 0, "Steamflareborn": 0, "Ironflareborn": 0, "Boltflareborn": 0,
    "Copperflareborn": 0, "Valveflareborn": 0, "Sootflareborn": 0, "Brassflareborn": 0, "Cogflareborn": 0,
    "Gearshroudgeist": 0, "Rustshroudgeist": 0, "Steamshroudgeist": 0, "Ironshroudgeist": 0, "Boltshroudgeist": 0,
    "Coppershroudgeist": 0, "Valveshroudgeist": 0, "Sootshroudgeist": 0, "Brassshroudgeist": 0, "Cogshroudgeist": 0,
    "Gearmiregeist": 0, "Rustmiregeist": 0, "Steammiregeist": 0, "Ironmiregeist": 0, "Boltmiregeist": 0,
    "Coppermiregeist": 0, "Valvemiregeist": 0, "Sootmiregeist": 0, "Brassmiregeist": 0, "Cogmiregeist": 0,
    "Geargritgeist": 0, "Rustgritgeist": 0, "Steamgritgeist": 0, "Irongritgeist": 0, "Boltgritgeist": 0,
    "Coppergritgeist": 0, "Valvegritgeist": 0, "Sootgritgeist": 0, "Brassgritgeist": 0, "Coggritgeist": 0,
    "Gearshalegeist": 0, "Rustshalegeist": 0, "Steamshalegeist": 0, "Ironshalegeist": 0, "Boltshalegeist": 0,
    "Coppershalegeist": 0, "Valveshalegeist": 0, "Sootshalegeist": 0, "Brassshalegeist": 0, "Cogshalegeist": 0,
    "Gearspiregeist": 0, "Rustspiregeist": 0, "Steamspiregeist": 0, "Ironspiregeist": 0, "Boltspiregeist": 0,
    "Copperspiregeist": 0, "Valvespiregeist": 0, "Sootspiregeist": 0, "Brassspiregeist": 0, "Cogspiregeist": 0,
    "Gearflareling": 0, "Rustflareling": 0, "Steamflareling": 0, "Ironflareling": 0, "Boltflareling": 0,
    "Copperflareling": 0, "Valveflareling": 0, "Sootflareling": 0, "Brassflareling": 0, "Cogflareling": 0,
    "Gearshroudspawn": 0, "Rustshroudspawn": 0, "Steamshroudspawn": 0, "Ironshroudspawn": 0, "Boltshroudspawn": 0,
    "Coppershroudspawn": 0, "Valveshroudspawn": 0, "Sootshroudspawn": 0, "Brassshroudspawn": 0, "Cogshroudspawn": 0,
    "Gearmirespawn": 0, "Rustmirespawn": 0, "Steammirespawn": 0, "Ironmirespawn": 0, "Boltmirespawn": 0,
    "Coppermirespawn": 0, "Valvemirespawn": 0, "Sootmirespawn": 0, "Brassmirespawn": 0, "Cogmirespawn": 0,
    "Geargritspawn": 0, "Rustgritspawn": 0, "Steamgritspawn": 0, "Irongritspawn": 0, "Boltgritspawn": 0,
    "Coppergritspawn": 0, "Valvegritspawn": 0, "Sootgritspawn": 0, "Brassgritspawn": 0, "Coggritspawn": 0,
    "Gearshalespawn": 0, "Rustshalespawn": 0, "Steamshalespawn": 0, "Ironshalespawn": 0, "Boltshalespawn": 0,
    "Coppershalespawn": 0, "Valveshalespawn": 0, "Sootshalespawn": 0, "Brassshalespawn": 0, "Cogshalespawn": 0,
    "Gearspirespawn": 0, "Rustspirespawn": 0, "Steamspirespawn": 0, "Ironspirespawn": 0, "Boltspirespawn": 0,
    "Copperspirespawn": 0, "Valvespirespawn": 0, "Sootspirespawn": 0, "Brassspirespawn": 0, "Cogspirespawn": 0
})


class EnemyNames:
    @staticmethod
    def ordinal(n: int) -> str:
        # Converts 2 → "2nd", 3 → "3rd", 4 → "4th", etc.
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    @staticmethod
    def stringify(name: str, count: int) -> str:
        # count = number of times the name has already appeared
        if count == 0:
            return name
        return f"{name} the {EnemyNames.ordinal(count + 1)}"

    @staticmethod
    def get_name() -> str:
        # choose a random base name
        name = random.choice(list(enemy_names.keys()))

        # get current usage count
        count = enemy_names[name]

        # increment for next time
        enemy_names[name] += 1

        # return the fully stringified version
        return EnemyNames.stringify(name, count)
