/**
 * FRACTAL ENGINE — MASTER PRESET BUILDER
 * Adobe After Effects ExtendScript (.jsx)
 *
 * Builds the full Fractal Engine rig documented in FractalEngine/README.md:
 * master comps, control hub, recursion/dynamo/torus/field-shell/aurora
 * expressions, HUD ritual layer, and camera — wired exactly as specified.
 *
 * HOW TO RUN
 *   File > Scripts > Run Script File...  and select this file.
 *   No file-system access is required, so no preference toggles are needed.
 *
 * WHAT YOU GET (all comps land in the Project panel)
 *   - FRACTAL_ENGINE_CTRL          control hub (sliders + checkbox)
 *   - FRACTAL_ENGINE_DYNAMO_CORE
 *   - FRACTAL_ENGINE_DYNAMO_TORUS
 *   - FRACTAL_ENGINE_FIELD_SHELL
 *   - FRACTAL_ENGINE_AURORA
 *   - FRACTAL_ENGINE_RECURSION     (8 duplicated placeholder layers)
 *   - FRACTAL_ENGINE_HUD_RITUAL
 *   - FRACTAL_ENGINE_MASTER_4K     (everything assembled, parented, + camera)
 *
 * The recursion/dynamo/torus/field/aurora layers are placeholder solids —
 * swap in your own fractal artwork or footage without touching the rig,
 * expressions, or parenting. Sound hooks and the VO line are written onto
 * FRACTAL_ENGINE_CTRL as a composition marker since no audio assets ship
 * with this script.
 */
(function buildFractalEngine() {

    app.beginUndoGroup("Build Fractal Engine");

    try {

        var W = 3840, H = 2160, FPS = 24, DUR = 30;
        var RECURSION_LAYERS = 8;

        function newComp(name, w, h) {
            return app.project.items.addComp(name, w || W, h || H, 1, DUR, FPS);
        }

        function addSlider(layer, fxName, value) {
            var fx = layer.Effects.addProperty("ADBE Slider Control");
            fx.name = fxName;
            fx.property(1).setValue(value);
            return fx;
        }

        function addCheckbox(layer, fxName, value) {
            var fx = layer.Effects.addProperty("ADBE Checkbox Control");
            fx.name = fxName;
            fx.property(1).setValue(value ? 1 : 0);
            return fx;
        }

        function solidLayer(comp, name, rgb01, w, h) {
            return comp.layers.addSolid(rgb01, name, w || comp.width, h || comp.height, 1, DUR);
        }

        // ---------------------------------------------------------------
        // 1. CONTROL HUB — FRACTAL_ENGINE_CTRL
        // ---------------------------------------------------------------
        var ctrlComp = newComp("FRACTAL_ENGINE_CTRL", 100, 100);
        var ctrlNull = ctrlComp.layers.addNull(DUR);
        ctrlNull.name = "FRACTAL_ENGINE_CTRL";
        addSlider(ctrlNull, "MACRO_SPEED", 1);
        addSlider(ctrlNull, "MESO_SPEED", 2);
        addSlider(ctrlNull, "SUB_SPEED", 3);
        addSlider(ctrlNull, "MICRO_SPEED", 4);
        addSlider(ctrlNull, "FIELD_INTENSITY", 50);
        addSlider(ctrlNull, "AURORA_RATE", 1);
        addSlider(ctrlNull, "RECURSION_DEPTH", 6);
        addSlider(ctrlNull, "PHASE_OFFSET", 10);
        addCheckbox(ctrlNull, "CEREMONIAL_MODE", false);

        ctrlComp.markerProperty.setValueAtTime(0, new MarkerValue(
            "SOUND HOOKS | low drone -> MACRO_SPEED | mid pulse -> AURORA_RATE | high shimmer -> RECURSION_DEPTH\n" +
            "VO HOOK | \"The plates turn. The recursion awakens. The engine remembers itself.\""
        ));

        // A single instance of the control hub is dropped into every comp
        // below (guide layer, so it never renders) so that its expressions'
        // thisComp.layer("FRACTAL_ENGINE_CTRL") lookups resolve locally.
        function addCtrlInstance(comp) {
            var l = comp.layers.add(ctrlComp);
            l.guideLayer = true;
            l.moveToEnd();
            return l;
        }

        // ---------------------------------------------------------------
        // 2. DYNAMO CORE — FRACTAL_ENGINE_DYNAMO_CORE
        // ---------------------------------------------------------------
        var dynamoCoreComp = newComp("FRACTAL_ENGINE_DYNAMO_CORE");
        addCtrlInstance(dynamoCoreComp);
        var dynamoCoreSolid = solidLayer(dynamoCoreComp, "Dynamo Core [placeholder]", [0.72, 0.08, 0.15], 1600, 1600);
        dynamoCoreSolid.property("Rotation").expression =
            'var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");\n' +
            'var macro = ctrl.effect("MACRO_SPEED")("Slider");\n' +
            'var meso = ctrl.effect("MESO_SPEED")("Slider");\n' +
            'var sub = ctrl.effect("SUB_SPEED")("Slider");\n' +
            'var micro = ctrl.effect("MICRO_SPEED")("Slider");\n' +
            '(time * (macro + meso + sub + micro)) * 10;';

        // ---------------------------------------------------------------
        // 3. TORUS (COUNTER-ROTATION) — FRACTAL_ENGINE_DYNAMO_TORUS
        // ---------------------------------------------------------------
        var torusComp = newComp("FRACTAL_ENGINE_DYNAMO_TORUS");
        addCtrlInstance(torusComp);
        var torusSolid = solidLayer(torusComp, "Torus [placeholder]", [0.85, 0.65, 0.13], 2200, 2200);
        torusSolid.property("Rotation").expression =
            'var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");\n' +
            'var sub = ctrl.effect("SUB_SPEED")("Slider");\n' +
            '-(time * sub * 15);';

        // ---------------------------------------------------------------
        // 4. FIELD SHELL — FRACTAL_ENGINE_FIELD_SHELL
        // ---------------------------------------------------------------
        var fieldComp = newComp("FRACTAL_ENGINE_FIELD_SHELL");
        addCtrlInstance(fieldComp);
        var fieldSolid = solidLayer(fieldComp, "Field Shell [placeholder]", [0.44, 0.11, 0.75], W, H);
        fieldSolid.property("Opacity").expression =
            'var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");\n' +
            'ctrl.effect("FIELD_INTENSITY")("Slider");';

        // ---------------------------------------------------------------
        // 5. AURORA (PULSE ENGINE) — FRACTAL_ENGINE_AURORA
        // ---------------------------------------------------------------
        var auroraComp = newComp("FRACTAL_ENGINE_AURORA");
        addCtrlInstance(auroraComp);
        var auroraSolid = solidLayer(auroraComp, "Aurora [placeholder]", [0.42, 0.24, 0.82], W, H);
        auroraSolid.property("Opacity").expression =
            'var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");\n' +
            'var rate = ctrl.effect("AURORA_RATE")("Slider");\n' +
            'var value = 40 + Math.sin(time * rate * 2) * 60;\n' +
            'var ceremonial = ctrl.effect("CEREMONIAL_MODE")("Checkbox");\n' +
            'ceremonial ? value + 20 : value;';

        // ---------------------------------------------------------------
        // 6. RECURSION LAYERS — FRACTAL_ENGINE_RECURSION
        // ---------------------------------------------------------------
        var recursionComp = newComp("FRACTAL_ENGINE_RECURSION");
        addCtrlInstance(recursionComp);
        var recursionRotationExpr =
            'var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");\n' +
            'var depth = ctrl.effect("RECURSION_DEPTH")("Slider");\n' +
            'var phase = ctrl.effect("PHASE_OFFSET")("Slider");\n' +
            'var speed = (index * 0.1) * depth;\n' +
            '(time * speed * 20) + (phase * index);';
        for (var i = 0; i < RECURSION_LAYERS; i++) {
            var scalePct = 90 - i * 9; // each duplicate nests slightly smaller
            var ring = solidLayer(recursionComp, "Recursion Layer " + (i + 1) + " [placeholder]",
                [0.1 + i * 0.05, 0.55, 0.85 - i * 0.05], W, H);
            ring.property("Scale").setValue([scalePct, scalePct]);
            ring.property("Rotation").expression = recursionRotationExpr;
        }

        // ---------------------------------------------------------------
        // 7. HUD RITUAL LAYER — FRACTAL_ENGINE_HUD_RITUAL
        // ---------------------------------------------------------------
        var hudComp = newComp("FRACTAL_ENGINE_HUD_RITUAL");
        addCtrlInstance(hudComp);
        var hudOpacityExpr =
            'var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");\n' +
            'ctrl.effect("CEREMONIAL_MODE")("Checkbox") ? 100 : 0;';

        var hudTitle = hudComp.layers.addText("Fractal Engine — Turning of All Plates");
        hudTitle.property("Position").setValue([W / 2, H / 2 - 80]);
        hudTitle.property("Opacity").expression = hudOpacityExpr;

        var hudSubtitle = hudComp.layers.addText("Macro → Meso → Sub → Micro → Consciousness");
        hudSubtitle.property("Position").setValue([W / 2, H / 2 + 20]);
        hudSubtitle.property("Opacity").expression = hudOpacityExpr;

        // ---------------------------------------------------------------
        // 8. MASTER COMP — FRACTAL_ENGINE_MASTER_4K
        // ---------------------------------------------------------------
        var masterComp = newComp("FRACTAL_ENGINE_MASTER_4K");

        var masterNull = masterComp.layers.addNull(DUR);
        masterNull.name = "FRACTAL_ENGINE_MASTER_NULL";

        // Assembly order per README (back to front): Dynamo Core, Torus,
        // Field Shell, Aurora, Recursion, HUD Ritual. layers.add() inserts
        // each new layer at the top of the stack, so adding in this order
        // leaves Dynamo Core at the back and HUD Ritual frontmost on top.
        var assemblyOrder = [dynamoCoreComp, torusComp, fieldComp, auroraComp, recursionComp, hudComp];
        for (var j = 0; j < assemblyOrder.length; j++) {
            var placedLayer = masterComp.layers.add(assemblyOrder[j]);
            placedLayer.parent = masterNull;
        }

        addCtrlInstance(masterComp);

        // ---------------------------------------------------------------
        // 9. CAMERA — slow orbital, slight dolly-in, 15% drift
        // ---------------------------------------------------------------
        var camRig = masterComp.layers.addNull(DUR);
        camRig.name = "FRACTAL_ENGINE_CAM_RIG";
        camRig.threeDLayer = true;
        camRig.parent = masterNull;
        camRig.property("Y Rotation").expression = "time * 4;"; // slow orbital
        camRig.property("Position").expression =
            'var base = value;\n' +
            'var driftNoise = wiggle(0.15, 40) - base;\n' + // organic drift source
            'var drift = driftNoise * 0.15;\n' + // 15% drift
            'var dollyIn = [0, 0, linear(time, 0, ' + DUR + ', 0, -600)];\n' +
            'base + drift + dollyIn;';

        var camera = masterComp.layers.addCamera("FRACTAL_ENGINE_CAM", [W / 2, H / 2]);
        camera.parent = camRig;

        alert("Fractal Engine built. \"" + masterComp.name + "\" is ready in the Project panel.");

    } catch (err) {
        alert("Fractal Engine build failed: " + err.toString() + " (line " + err.line + ")");
    }

    app.endUndoGroup();

})();
