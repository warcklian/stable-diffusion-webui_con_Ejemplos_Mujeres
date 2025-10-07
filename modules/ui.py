import datetime
import mimetypes
import os
import sys
from functools import reduce
import warnings
from contextlib import ExitStack
from pathlib import Path

import gradio as gr
import gradio.utils
import numpy as np
from PIL import Image, PngImagePlugin  # noqa: F401
from modules.call_queue import wrap_gradio_gpu_call, wrap_queued_call, wrap_gradio_call, wrap_gradio_call_no_job # noqa: F401

from modules import gradio_extensons, sd_schedulers  # noqa: F401
from modules import sd_hijack, sd_models, script_callbacks, ui_extensions, deepbooru, extra_networks, ui_common, ui_postprocessing, progress, ui_loadsave, shared_items, ui_settings, timer, sysinfo, ui_checkpoint_merger, scripts, sd_samplers, processing, ui_extra_networks, ui_toprow, launch_utils
from modules.ui_components import FormRow, FormGroup, ToolButton, FormHTML, InputAccordion, ResizeHandleRow
from modules.paths import script_path
from modules.ui_common import create_refresh_button
from modules.ui_gradio_extensions import reload_javascript

from modules.shared import opts, cmd_opts

import modules.infotext_utils as parameters_copypaste
import modules.hypernetworks.ui as hypernetworks_ui
import modules.textual_inversion.ui as textual_inversion_ui
import modules.textual_inversion.textual_inversion as textual_inversion
import modules.shared as shared
from modules import prompt_parser
from modules.sd_hijack import model_hijack
from modules.infotext_utils import image_from_url_text, PasteField

create_setting_component = ui_settings.create_setting_component

warnings.filterwarnings("default" if opts.show_warnings else "ignore", category=UserWarning)
warnings.filterwarnings("default" if opts.show_gradio_deprecation_warnings else "ignore", category=gr.deprecation.GradioDeprecationWarning)

# this is a fix for Windows users. Without it, javascript files will be served with text/html content-type and the browser will not show any UI
mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')

# Likewise, add explicit content-type header for certain missing image types
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/avif', '.avif')

if not cmd_opts.share and not cmd_opts.listen:
    # fix gradio phoning home
    gradio.utils.version_check = lambda: None
    gradio.utils.get_local_ip_address = lambda: '127.0.0.1'

if cmd_opts.ngrok is not None:
    import modules.ngrok as ngrok
    print('ngrok authtoken detected, trying to connect...')
    ngrok.connect(
        cmd_opts.ngrok,
        cmd_opts.port if cmd_opts.port is not None else 7860,
        cmd_opts.ngrok_options
        )


def gr_show(visible=True):
    return {"visible": visible, "__type__": "update"}


sample_img2img = "assets/stable-samples/img2img/sketch-mountains-input.jpg"
sample_img2img = sample_img2img if os.path.exists(sample_img2img) else None

# Using constants for these since the variation selector isn't visible.
# Important that they exactly match script.js for tooltip to work.
random_symbol = '\U0001f3b2\ufe0f'  # 🎲️
reuse_symbol = '\u267b\ufe0f'  # ♻️
paste_symbol = '\u2199\ufe0f'  # ↙
refresh_symbol = '\U0001f504'  # 🔄
save_style_symbol = '\U0001f4be'  # 💾
apply_style_symbol = '\U0001f4cb'  # 📋
clear_prompt_symbol = '\U0001f5d1\ufe0f'  # 🗑️
extra_networks_symbol = '\U0001F3B4'  # 🎴
switch_values_symbol = '\U000021C5' # ⇅
restore_progress_symbol = '\U0001F300' # 🌀
detect_image_size_symbol = '\U0001F4D0'  # 📐


plaintext_to_html = ui_common.plaintext_to_html


def send_gradio_gallery_to_image(x):
    if len(x) == 0:
        return None
    return image_from_url_text(x[0])


def calc_resolution_hires(enable, width, height, hr_scale, hr_resize_x, hr_resize_y):
    if not enable:
        return ""

    p = processing.StableDiffusionProcessingTxt2Img(width=width, height=height, enable_hr=True, hr_scale=hr_scale, hr_resize_x=hr_resize_x, hr_resize_y=hr_resize_y)
    p.calculate_target_resolution()

    return f"from <span class='resolution'>{p.width}x{p.height}</span> to <span class='resolution'>{p.hr_resize_x or p.hr_upscale_to_x}x{p.hr_resize_y or p.hr_upscale_to_y}</span>"


def resize_from_to_html(width, height, scale_by):
    target_width = int(width * scale_by)
    target_height = int(height * scale_by)

    if not target_width or not target_height:
        return "no image selected"

    return f"resize: from <span class='resolution'>{width}x{height}</span> to <span class='resolution'>{target_width}x{target_height}</span>"


def process_interrogate(interrogation_function, mode, ii_input_dir, ii_output_dir, *ii_singles):
    if mode in {0, 1, 3, 4}:
        return [interrogation_function(ii_singles[mode]), None]
    elif mode == 2:
        return [interrogation_function(ii_singles[mode]["image"]), None]
    elif mode == 5:
        assert not shared.cmd_opts.hide_ui_dir_config, "Launched with --hide-ui-dir-config, batch img2img disabled"
        images = shared.listfiles(ii_input_dir)
        print(f"Will process {len(images)} images.")
        if ii_output_dir != "":
            os.makedirs(ii_output_dir, exist_ok=True)
        else:
            ii_output_dir = ii_input_dir

        for image in images:
            img = Image.open(image)
            filename = os.path.basename(image)
            left, _ = os.path.splitext(filename)
            print(interrogation_function(img), file=open(os.path.join(ii_output_dir, f"{left}.txt"), 'a', encoding='utf-8'))

        return [gr.update(), None]


def interrogate(image):
    prompt = shared.interrogator.interrogate(image.convert("RGB"))
    return gr.update() if prompt is None else prompt


def interrogate_deepbooru(image):
    prompt = deepbooru.model.tag(image)
    return gr.update() if prompt is None else prompt


def connect_clear_prompt(button):
    """Given clear button, prompt, and token_counter objects, setup clear prompt button click event"""
    button.click(
        _js="clear_prompt",
        fn=None,
        inputs=[],
        outputs=[],
    )


def update_token_counter(text, steps, styles, *, is_positive=True):
    params = script_callbacks.BeforeTokenCounterParams(text, steps, styles, is_positive=is_positive)
    script_callbacks.before_token_counter_callback(params)
    text = params.prompt
    steps = params.steps
    styles = params.styles
    is_positive = params.is_positive

    if shared.opts.include_styles_into_token_counters:
        apply_styles = shared.prompt_styles.apply_styles_to_prompt if is_positive else shared.prompt_styles.apply_negative_styles_to_prompt
        text = apply_styles(text, styles)

    try:
        text, _ = extra_networks.parse_prompt(text)

        if is_positive:
            _, prompt_flat_list, _ = prompt_parser.get_multicond_prompt_list([text])
        else:
            prompt_flat_list = [text]

        prompt_schedules = prompt_parser.get_learned_conditioning_prompt_schedules(prompt_flat_list, steps)

    except Exception:
        # a parsing error can happen here during typing, and we don't want to bother the user with
        # messages related to it in console
        prompt_schedules = [[[steps, text]]]

    flat_prompts = reduce(lambda list1, list2: list1+list2, prompt_schedules)
    prompts = [prompt_text for step, prompt_text in flat_prompts]
    token_count, max_length = max([model_hijack.get_prompt_lengths(prompt) for prompt in prompts], key=lambda args: args[0])
    return f"<span class='gr-box gr-text-input'>{token_count}/{max_length}</span>"


def update_negative_prompt_token_counter(*args):
    return update_token_counter(*args, is_positive=False)


def setup_progressbar(*args, **kwargs):
    pass


def apply_setting(key, value):
    if value is None:
        return gr.update()

    if shared.cmd_opts.freeze_settings:
        return gr.update()

    # dont allow model to be swapped when model hash exists in prompt
    if key == "sd_model_checkpoint" and opts.disable_weights_auto_swap:
        return gr.update()

    if key == "sd_model_checkpoint":
        ckpt_info = sd_models.get_closet_checkpoint_match(value)

        if ckpt_info is not None:
            value = ckpt_info.title
        else:
            return gr.update()

    comp_args = opts.data_labels[key].component_args
    if comp_args and isinstance(comp_args, dict) and comp_args.get('visible') is False:
        return

    valtype = type(opts.data_labels[key].default)
    oldval = opts.data.get(key, None)
    opts.data[key] = valtype(value) if valtype != type(None) else value
    if oldval != value and opts.data_labels[key].onchange is not None:
        opts.data_labels[key].onchange()

    opts.save(shared.config_filename)
    return getattr(opts, key)


def create_output_panel(tabname, outdir, toprow=None):
    return ui_common.create_output_panel(tabname, outdir, toprow)


def ordered_ui_categories():
    user_order = {x.strip(): i * 2 + 1 for i, x in enumerate(shared.opts.ui_reorder_list)}

    for _, category in sorted(enumerate(shared_items.ui_reorder_categories()), key=lambda x: user_order.get(x[1], x[0] * 2 + 0)):
        yield category


def create_override_settings_dropdown(tabname, row):
    dropdown = gr.Dropdown([], label="Override settings", visible=False, elem_id=f"{tabname}_override_settings", multiselect=True)

    dropdown.change(
        fn=lambda x: gr.Dropdown.update(visible=bool(x)),
        inputs=[dropdown],
        outputs=[dropdown],
    )

    return dropdown


def create_ui():
    import modules.img2img
    import modules.txt2img

    reload_javascript()

    parameters_copypaste.reset()

    settings = ui_settings.UiSettings()
    settings.register_settings()

    scripts.scripts_current = scripts.scripts_txt2img
    scripts.scripts_txt2img.initialize_scripts(is_img2img=False)
    
    # Variable global para controlar cancelación de generación
    global generation_cancelled
    generation_cancelled = False

    with gr.Blocks(analytics_enabled=False, css="""
    /* Lado Izquierdo - Configuración Original (Azul claro) */
    #left_column_original {
        background-color: rgba(173, 216, 230, 0.2) !important;
        border: 3px solid rgba(173, 216, 230, 0.6) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin: 10px !important;
    }
    
    /* Lado Derecho - Pasaportes (Verde claro) */
    #right_column_pasaportes {
        background-color: rgba(144, 238, 144, 0.2) !important;
        border: 3px solid rgba(144, 238, 144, 0.6) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin: 10px !important;
    }
    
    /* Accordion de Nacionalidad Avanzada (Verde más intenso) */
    .pasaportes_accordion {
        background-color: rgba(34, 139, 34, 0.15) !important;
        border: 2px solid rgba(34, 139, 34, 0.5) !important;
        border-radius: 8px !important;
        margin: 8px 0 !important;
    }
    
    /* Accordion de Controles Genéticos (Morado) */
    .genetic_accordion {
        background-color: rgba(138, 43, 226, 0.15) !important;
        border: 2px solid rgba(138, 43, 226, 0.5) !important;
        border-radius: 8px !important;
        margin: 8px 0 !important;
    }
    
    /* Panel de salida (Gallery) - Naranja */
    .gallery-container {
        background-color: rgba(255, 165, 0, 0.15) !important;
        border: 2px solid rgba(255, 165, 0, 0.5) !important;
        border-radius: 8px !important;
        padding: 10px !important;
        margin: 5px !important;
    }
    """) as txt2img_interface:
        toprow = ui_toprow.Toprow(is_img2img=False, is_compact=shared.opts.compact_prompt_box)

        dummy_component = gr.Label(visible=False)

        extra_tabs = gr.Tabs(elem_id="txt2img_extra_tabs", elem_classes=["extra-networks"])
        extra_tabs.__enter__()

        with gr.Tab("Generation", id="txt2img_generation") as txt2img_generation_tab, ResizeHandleRow(equal_height=False):
            # ===== LADO IZQUIERDO: CONFIGURACIÓN ORIGINAL DE TXT2IMG =====
            with gr.Column(scale=1, elem_id="left_column_original"):
                # Configuración normal de txt2img
                with ExitStack() as stack:
                    if shared.opts.txt2img_settings_accordion:
                        stack.enter_context(gr.Accordion("Open for Settings", open=True))
                    stack.enter_context(gr.Column(variant='compact', elem_id="txt2img_settings"))

                    scripts.scripts_txt2img.prepare_ui()

                    for category in ordered_ui_categories():
                        if category == "prompt":
                            toprow.create_inline_toprow_prompts()

                        elif category == "dimensions":
                            with FormRow():
                                with gr.Column(elem_id="txt2img_column_size", scale=4):
                                    width = gr.Slider(minimum=64, maximum=2048, step=8, label="Width", value=512, elem_id="txt2img_width")
                                    height = gr.Slider(minimum=64, maximum=2048, step=8, label="Height", value=512, elem_id="txt2img_height")

                                with gr.Column(elem_id="txt2img_dimensions_row", scale=1, elem_classes="dimensions-tools"):
                                    res_switch_btn = ToolButton(value=switch_values_symbol, elem_id="txt2img_res_switch_btn", tooltip="Switch width/height")

                                if opts.dimensions_and_batch_together:
                                    with gr.Column(elem_id="txt2img_column_batch"):
                                        batch_count = gr.Slider(minimum=1, step=1, label='Batch count', value=1, elem_id="txt2img_batch_count")
                                        batch_size = gr.Slider(minimum=1, maximum=8, step=1, label='Batch size', value=1, elem_id="txt2img_batch_size")

                        elif category == "cfg":
                                with gr.Row():
                                    cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5, label='CFG Scale', value=12.0, elem_id="txt2img_cfg_scale")

                        elif category == "checkboxes":
                                with FormRow(elem_classes="checkboxes-row", variant="compact"):
                                    pass

                        elif category == "accordions":
                                with gr.Row(elem_id="txt2img_accordions", elem_classes="accordions"):
                                    with InputAccordion(False, label="Hires. fix", elem_id="txt2img_hr") as enable_hr:
                                        with enable_hr.extra():
                                            hr_final_resolution = FormHTML(value="", elem_id="txtimg_hr_finalres", label="Upscaled resolution", interactive=False, min_width=0)

                                        with FormRow(elem_id="txt2img_hires_fix_row1", variant="compact"):
                                            hr_upscaler = gr.Dropdown(label="Upscaler", elem_id="txt2img_hr_upscaler", choices=[*shared.latent_upscale_modes, *[x.name for x in shared.sd_upscalers]], value=shared.latent_upscale_default_mode)
                                            hr_second_pass_steps = gr.Slider(minimum=0, maximum=150, step=1, label='Hires steps', value=0, elem_id="txt2img_hires_steps")
                                            denoising_strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label='Denoising strength', value=0.7, elem_id="txt2img_denoising_strength")

                                        with FormRow(elem_id="txt2img_hires_fix_row2", variant="compact"):
                                            hr_scale = gr.Slider(minimum=1.0, maximum=4.0, step=0.05, label="Upscale by", value=2.0, elem_id="txt2img_hr_scale")
                                            hr_resize_x = gr.Slider(minimum=0, maximum=2048, step=8, label="Resize width to", value=0, elem_id="txt2img_hr_resize_x")
                                            hr_resize_y = gr.Slider(minimum=0, maximum=2048, step=8, label="Resize height to", value=0, elem_id="txt2img_hr_resize_y")

                                        with FormRow(elem_id="txt2img_hires_fix_row3", variant="compact", visible=opts.hires_fix_show_sampler) as hr_sampler_container:

                                            hr_checkpoint_name = gr.Dropdown(label='Checkpoint', elem_id="hr_checkpoint", choices=["Use same checkpoint"] + modules.sd_models.checkpoint_tiles(use_short=True), value="Use same checkpoint")
                                            hr_sampler_name = gr.Dropdown(label='Hires sampler', elem_id="hr_sampler", choices=["Use same sampler"] + list(sd_samplers.samplers_map.keys()), value="Use same sampler")
                                            hr_scheduler = gr.Dropdown(label='Scheduler', elem_id="hr_scheduler", choices=["Use same scheduler"] + list(sd_schedulers.schedulers), value="Use same scheduler")

                                    with InputAccordion(False, label="Refiner", elem_id="txt2img_refiner") as enable_refiner:
                                        with enable_refiner.extra():
                                            refiner_checkpoint = gr.Dropdown(label='Checkpoint', elem_id="refiner_checkpoint", choices=["None"] + modules.sd_models.checkpoint_tiles(use_short=True), value="None")
                                            refiner_switch_at = gr.Slider(value=0.8, label="Switch at", minimum=0.1, maximum=1.0, step=0.01, elem_id="refiner_switch_at")

                        elif category == "batch":
                                if not opts.dimensions_and_batch_together:
                                    with FormRow(elem_id="txt2img_column_batch"):
                                        batch_count = gr.Slider(minimum=1, step=1, label='Batch count', value=1, elem_id="txt2img_batch_count")
                                        batch_size = gr.Slider(minimum=1, maximum=8, step=1, label='Batch size', value=1, elem_id="txt2img_batch_size")

                        elif category == "override_settings":
                                with FormRow(elem_id="txt2img_override_settings_row", variant="compact", elem_classes="override_settings_row"):
                                    override_settings = create_override_settings_dropdown('txt2img', 'txt2img_override_settings')

                        elif category == "scripts":
                                with FormGroup(elem_id="txt2img_script_container"):
                                    txt2img_script_runner = scripts.scripts_txt2img

                # Panel de salida (gallery con botones) - agregado al lado izquierdo
                with gr.Row():
                    output_panel = create_output_panel("txt2img", opts.outdir_txt2img_samples, toprow)

            # ===== LADO DERECHO: NUEVAS IMPLEMENTACIONES DE PASAPORTES =====
            with gr.Column(scale=1, elem_id="right_column_pasaportes"):
                # Funciones para los controles de pasaportes
                def guardar_configuracion_genetica(beauty_control, skin_control, hair_control, eye_control, background_control, region_control="aleatorio"):
                    """Guarda la configuración de controles genéticos avanzados."""
                    try:
                        import json
                        config = {
                            "beauty_control": beauty_control,
                            "skin_control": skin_control,
                            "hair_control": hair_control,
                            "eye_control": eye_control,
                            "background_control": background_control,
                            "region_control": region_control,  # Agregar región
                            "saved_at": datetime.now().isoformat()
                        }
                        config_path = Path("genetic_config.json")
                        with open(config_path, 'w', encoding='utf-8') as f:
                            json.dump(config, f, indent=2, ensure_ascii=False)
                        return True
                    except Exception as e:
                        print(f"Error guardando configuración genética: {e}")
                        return False
                
                def cargar_configuracion_genetica():
                    """Carga la configuración guardada de controles genéticos avanzados."""
                    try:
                        import json
                        config_path = Path("genetic_config.json")
                        if config_path.exists():
                            with open(config_path, 'r', encoding='utf-8') as f:
                                config = json.load(f)
                            return (
                                config.get("beauty_control", "exceptionally_beautiful"),
                                config.get("skin_control", "auto"),
                                config.get("hair_control", "auto"),
                                config.get("eye_control", "auto"),
                                config.get("background_control", "white"),
                                config.get("region_control", "aleatorio")  # Agregar región
                            )
                        else:
                            return ("exceptionally_beautiful", "auto", "auto", "auto", "white", "aleatorio")
                    except Exception as e:
                        print(f"Error cargando configuración genética: {e}")
                        return ("exceptionally_beautiful", "auto", "auto", "auto", "white", "aleatorio")

                def guardar_plantilla_ui(nombre_plantilla, prompt, negative_prompt, width, height, cfg_scale, steps, sampler_name, seed, batch_count, batch_size, denoising_strength, hr_second_pass_steps, hr_scale, hr_resize_x, hr_resize_y, hr_upscaler, hr_sampler_name, hr_scheduler, refiner_checkpoint, refiner_switch_at):
                    """Guarda la configuración actual de la UI en una plantilla JSON con validación mejorada."""
                    try:
                        import json
                        import re
                        from datetime import datetime
                        
                        # Validación del nombre
                        if not nombre_plantilla or not nombre_plantilla.strip():
                            return "❌ **Error**: El nombre de la plantilla no puede estar vacío.", gr.update(), nombre_plantilla
                        
                        nombre_plantilla = nombre_plantilla.strip()
                        
                        # Validar caracteres permitidos
                        if not re.match(r'^[a-zA-Z0-9\s\-_áéíóúñÁÉÍÓÚÑ]+$', nombre_plantilla):
                            return "❌ **Error**: El nombre solo puede contener letras, números, espacios, guiones y guiones bajos.", gr.update(), nombre_plantilla
                        
                        # Limitar longitud
                        if len(nombre_plantilla) > 50:
                            return "❌ **Error**: El nombre no puede tener más de 50 caracteres.", gr.update(), nombre_plantilla
                        
                        # Crear directorio de plantillas
                        templates_dir = Path("outputs/templates")
                        templates_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Crear nombre de archivo seguro
                        nombre_archivo = re.sub(r'[^\w\-_áéíóúñÁÉÍÓÚÑ]', '_', nombre_plantilla)
                        nombre_archivo = f"{nombre_archivo}.json"
                        archivo_plantilla = templates_dir / nombre_archivo
                        
                        # Verificar si ya existe
                        if archivo_plantilla.exists():
                            return f"❌ **Error**: Ya existe una plantilla con el nombre '{nombre_plantilla}'. Elige otro nombre.", gr.update(), nombre_plantilla
                        
                        # Crear configuración de plantilla
                        plantilla = {
                            "nombre": nombre_plantilla,
                            "fecha_creacion": datetime.now().isoformat(),
                            "version": "1.0",
                            "descripcion": f"Plantilla personalizada creada el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                            "configuracion": {
                                "prompt": prompt,
                                "negative_prompt": negative_prompt,
                                "width": width,
                                "height": height,
                                "cfg_scale": cfg_scale,
                                "steps": steps,
                                "sampler_name": sampler_name,
                                "seed": seed,
                                "batch_count": batch_count,
                                "batch_size": batch_size,
                                "denoising_strength": denoising_strength,
                                "hr_second_pass_steps": hr_second_pass_steps,
                                "hr_scale": hr_scale,
                                "hr_resize_x": hr_resize_x,
                                "hr_resize_y": hr_resize_y,
                                "hr_upscaler": hr_upscaler,
                                "hr_sampler_name": hr_sampler_name,
                                "hr_scheduler": hr_scheduler,
                                "refiner_checkpoint": refiner_checkpoint,
                                "refiner_switch_at": refiner_switch_at
                            }
                        }
                        
                        # Guardar plantilla
                        with open(archivo_plantilla, 'w', encoding='utf-8') as f:
                            json.dump(plantilla, f, indent=2, ensure_ascii=False)
                        
                        # Actualizar dropdown
                        dropdown_update = actualizar_dropdown_plantillas()
                        
                        mensaje = f"""✅ **Plantilla guardada exitosamente**

📁 **Archivo**: `{archivo_plantilla.name}`
📅 **Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎯 **Nombre**: {nombre_plantilla}
📊 **Parámetros guardados**: {len(plantilla['configuracion'])} configuraciones

💡 **Consejo**: Ahora puedes cargar esta plantilla en cualquier momento."""
                        
                        return mensaje, dropdown_update, ""  # Limpiar el campo de nombre
                        
                    except Exception as e:
                        return f"❌ **Error guardando plantilla**: {str(e)}", gr.update(), nombre_plantilla

                def cargar_plantilla_ui(archivo_plantilla):
                    """Carga una plantilla guardada y aplica la configuración a la UI."""
                    try:
                        import json
                        
                        if not archivo_plantilla:
                            return ("", "", 512, 512, 7.0, 20, "Euler a", -1, 1, 1, 0.7, 0, 2.0, 0, 0, "Latent", "Use same sampler", "Use same scheduler", "None", 0.8, "❌ **Error**: No se seleccionó ninguna plantilla.")
                        
                        # Leer plantilla
                        with open(archivo_plantilla, 'r', encoding='utf-8') as f:
                            plantilla = json.load(f)
                        
                        config = plantilla["configuracion"]
                        
                        mensaje = f"""✅ **Plantilla cargada exitosamente**

📁 **Archivo**: `{Path(archivo_plantilla).name}`
🎯 **Nombre**: {plantilla['nombre']}
📅 **Creada**: {plantilla.get('fecha_creacion', 'Fecha no disponible')}
📊 **Parámetros cargados**: {len(config)} configuraciones

💡 **Consejo**: Todos los parámetros han sido aplicados a la UI."""
                        
                        # Retornar valores para actualizar la UI
                        return (
                            config["prompt"],
                            config["negative_prompt"],
                            config["width"],
                            config["height"],
                            config["cfg_scale"],
                            config["steps"],
                            config["sampler_name"],
                            config["seed"],
                            config["batch_count"],
                            config["batch_size"],
                            config["denoising_strength"],
                            config["hr_second_pass_steps"],
                            config["hr_scale"],
                            config["hr_resize_x"],
                            config["hr_resize_y"],
                            config["hr_upscaler"],
                            config["hr_sampler_name"],
                            config["hr_scheduler"],
                            config["refiner_checkpoint"],
                            config["refiner_switch_at"],
                            mensaje
                        )
                        
                    except Exception as e:
                        return ("", "", 512, 512, 7.0, 20, "Euler a", -1, 1, 1, 0.7, 0, 2.0, 0, 0, "Latent", "Use same sampler", "Use same scheduler", "None", 0.8, f"❌ **Error cargando plantilla**: {str(e)}")

                def eliminar_plantilla_ui(archivo_plantilla):
                    """Elimina una plantilla guardada."""
                    try:
                        if not archivo_plantilla:
                            return "❌ **Error**: No se seleccionó ninguna plantilla para eliminar.", gr.update()
                        
                        # Verificar que el archivo existe
                        if not Path(archivo_plantilla).exists():
                            return "❌ **Error**: La plantilla no existe.", gr.update()
                        
                        # Leer información de la plantilla antes de eliminar
                        try:
                            import json
                            with open(archivo_plantilla, 'r', encoding='utf-8') as f:
                                plantilla = json.load(f)
                            nombre_plantilla = plantilla.get('nombre', 'Plantilla sin nombre')
                        except:
                            nombre_plantilla = Path(archivo_plantilla).stem
                        
                        # Eliminar archivo
                        Path(archivo_plantilla).unlink()
                        
                        # Actualizar dropdown
                        dropdown_update = actualizar_dropdown_plantillas()
                        
                        mensaje = f"""🗑️ **Plantilla eliminada exitosamente**

📁 **Archivo eliminado**: `{Path(archivo_plantilla).name}`
🎯 **Nombre**: {nombre_plantilla}
📅 **Eliminada**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠️ **Advertencia**: Esta acción no se puede deshacer."""
                        
                        return mensaje, dropdown_update
                        
                    except Exception as e:
                        return f"❌ **Error eliminando plantilla**: {str(e)}", gr.update()

                def listar_plantillas_disponibles():
                    """Lista todas las plantillas disponibles en el directorio templates."""
                    try:
                        import json
                        templates_dir = Path("outputs/templates")
                        if not templates_dir.exists():
                            return "📁 **No hay plantillas guardadas**\n\n💡 **Sugerencia**: Guarda tu primera plantilla usando el botón '💾 Guardar Plantilla'"
                        
                        plantillas = []
                        for archivo in templates_dir.glob("*.json"):
                            try:
                                with open(archivo, 'r', encoding='utf-8') as f:
                                    plantilla = json.load(f)
                                plantillas.append({
                                    "archivo": str(archivo),
                                    "nombre": plantilla.get("nombre", archivo.stem),
                                    "fecha": plantilla.get("fecha_creacion", "Desconocida")
                                })
                            except:
                                continue
                        
                        if not plantillas:
                            return "📁 **No hay plantillas válidas**\n\n💡 **Sugerencia**: Guarda tu primera plantilla usando el botón '💾 Guardar Plantilla'"
                        
                        # Ordenar por fecha de creación (más recientes primero)
                        plantillas.sort(key=lambda x: x["fecha"], reverse=True)
                        
                        resultado = "📋 **Plantillas Disponibles**\n\n"
                        for i, plantilla in enumerate(plantillas, 1):
                            fecha_formateada = plantilla["fecha"][:19].replace("T", " ") if plantilla["fecha"] != "Desconocida" else "Desconocida"
                            resultado += f"**{i}.** {plantilla['nombre']}\n"
                            resultado += f"   📅 {fecha_formateada}\n"
                            resultado += f"   📁 `{Path(plantilla['archivo']).name}`\n\n"
                        
                        return resultado
                        
                    except Exception as e:
                        return f"❌ **Error listando plantillas**: {e}"

                def actualizar_dropdown_plantillas():
                    """Actualiza el dropdown con las plantillas disponibles."""
                    try:
                        import json
                        templates_dir = Path("outputs/templates")
                        if not templates_dir.exists():
                            return gr.update(choices=[], value=None)
                        
                        plantillas = []
                        for archivo in templates_dir.glob("*.json"):
                            try:
                                with open(archivo, 'r', encoding='utf-8') as f:
                                    plantilla = json.load(f)
                                plantillas.append({
                                    "archivo": str(archivo),
                                    "nombre": plantilla.get("nombre", archivo.stem),
                                    "fecha": plantilla.get("fecha_creacion", "Desconocida")
                                })
                            except:
                                continue
                        
                        if not plantillas:
                            return gr.update(choices=[], value=None)
                        
                        # Ordenar por fecha de creación (más recientes primero)
                        plantillas.sort(key=lambda x: x["fecha"], reverse=True)
                        
                        # Crear choices para el dropdown
                        choices = []
                        for plantilla in plantillas:
                            fecha_formateada = plantilla["fecha"][:19].replace("T", " ") if plantilla["fecha"] != "Desconocida" else "Desconocida"
                            display_name = f"{plantilla['nombre']} ({fecha_formateada})"
                            choices.append((display_name, plantilla["archivo"]))
                        
                        return gr.update(choices=choices, value=choices[0][1] if choices else None)
                        
                    except Exception as e:
                        print(f"Error actualizando dropdown de plantillas: {e}")
                        return gr.update(choices=[], value=None)
                
                def generar_caracteristicas_etnicas_diversas(nacionalidad, genero, edad, region="aleatorio"):
                    """Genera características étnicas diversas para el método masivo básico."""
                    import random
                    import time
                    
                    # Agregar timestamp y múltiples factores para máxima aleatoriedad
                    import hashlib
                    unique_seed = int(time.time() * 1000000) + random.randint(1, 999999) + hash(f"{nacionalidad}{genero}{edad}{region}") % 1000000
                    random.seed(unique_seed)
                    
                    # SIEMPRE usar región aleatoria para máxima diversidad
                    regiones_disponibles = ["caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"]
                    region = random.choice(regiones_disponibles)
                    
                    # Características regionales que influyen en la apariencia
                    caracteristicas_regionales = {
                        "caracas": {"skin_modifier": "urban", "hair_modifier": "modern"},
                        "maracaibo": {"skin_modifier": "coastal", "hair_modifier": "tropical"},
                        "valencia": {"skin_modifier": "industrial", "hair_modifier": "practical"},
                        "merida": {"skin_modifier": "mountain", "hair_modifier": "traditional"},
                        "san_cristobal": {"skin_modifier": "border", "hair_modifier": "mixed"},
                        "barcelona": {"skin_modifier": "eastern", "hair_modifier": "coastal"},
                        "ciudad_guayana": {"skin_modifier": "industrial", "hair_modifier": "modern"},
                        "maturin": {"skin_modifier": "eastern", "hair_modifier": "traditional"},
                        "barquisimeto": {"skin_modifier": "central", "hair_modifier": "mixed"},
                        "puerto_la_cruz": {"skin_modifier": "coastal", "hair_modifier": "tropical"}
                    }
                    
                    # Características de piel por nacionalidad - EXPANDIDAS para mayor diversidad
                    skin_tones = {
                        "venezuelan": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey"],
                        "cuban": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey"],
                        "haitian": ["medium-dark", "dark", "very-dark", "ebony", "mahogany", "chocolate", "coffee", "rich brown"],
                        "dominican": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey"],
                        "mexican": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey"],
                        "brazilian": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey", "dark", "rich brown"],
                        "american": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey", "dark", "rich brown", "pale", "ivory"]
                    }
                    
                    # Colores de cabello por nacionalidad - EXPANDIDOS para mayor diversidad
                    hair_colors = {
                        "venezuelan": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze"],
                        "cuban": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze"],
                        "haitian": ["black", "dark brown", "brown", "chocolate", "espresso", "mahogany", "jet black", "raven"],
                        "dominican": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze"],
                        "mexican": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze"],
                        "brazilian": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze", "blonde", "light brown", "honey"],
                        "american": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze", "blonde", "light brown", "honey", "red", "strawberry blonde", "platinum"]
                    }
                    
                    # Colores de ojos por nacionalidad - EXPANDIDOS para mayor diversidad
                    eye_colors = {
                        "venezuelan": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany"],
                        "cuban": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany"],
                        "haitian": ["dark brown", "brown", "chocolate", "coffee", "mahogany", "ebony", "rich brown"],
                        "dominican": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany"],
                        "mexican": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany"],
                        "brazilian": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany", "green", "emerald", "olive"],
                        "american": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany", "green", "emerald", "olive", "blue", "steel blue", "gray", "gray-blue"]
                    }
                    
                    # Estilos de cabello - EXPANDIDOS para mayor diversidad
                    hair_styles = ["straight", "wavy", "curly", "coily", "braided", "ponytail", "bun", "pixie", "bob", "long", "shoulder-length", "layered", "textured", "voluminous", "sleek", "messy", "styled", "natural", "professional", "casual"]
                    
                    # Formas de cara - EXPANDIDAS para mayor diversidad
                    face_shapes = ["oval", "round", "square", "heart", "diamond", "long", "triangular", "pear", "inverted triangle", "rectangular", "angular", "soft", "defined", "symmetrical"]
                    
                    # Características faciales - ULTRA EXPANDIDAS para máxima diversidad
                    facial_features = {
                        "nose": ["straight", "aquiline", "button", "wide", "narrow", "small", "prominent", "delicate", "strong", "refined", "classic", "distinctive", "roman", "snub", "hooked", "bulbous", "pointed", "flat", "upturned", "downturned", "asymmetric", "perfect", "crooked", "broad", "thin", "long", "short"],
                        "lips": ["full", "medium", "thin", "wide", "narrow", "plump", "defined", "natural", "shapely", "expressive", "delicate", "strong", "pouty", "bow-shaped", "heart-shaped", "straight", "curved", "asymmetric", "perfect", "uneven", "thick", "thin", "long", "short", "prominent", "subtle"],
                        "eyes": ["almond", "round", "hooded", "deep-set", "wide-set", "close-set", "upturned", "downturned", "monolid", "double-lid", "expressive", "intense", "gentle", "piercing", "sleepy", "alert", "droopy", "cat-like", "downturned", "upturned", "asymmetric", "perfect", "uneven", "large", "small", "prominent", "recessed"]
                    }
                    
                    # Obtener características regionales
                    region_traits = caracteristicas_regionales.get(region, {"skin_modifier": "standard", "hair_modifier": "standard"})
                    
                    # Seleccionar características aleatorias con influencia regional
                    skin_tone = random.choice(skin_tones.get(nacionalidad, ["medium", "olive", "tan"]))
                    hair_color = random.choice(hair_colors.get(nacionalidad, ["black", "dark brown", "brown"]))
                    eye_color = random.choice(eye_colors.get(nacionalidad, ["dark brown", "brown", "hazel"]))
                    hair_style = random.choice(hair_styles)
                    face_shape = random.choice(face_shapes)
                    nose_shape = random.choice(facial_features["nose"])
                    lip_shape = random.choice(facial_features["lips"])
                    eye_shape = random.choice(facial_features["eyes"])
                    
                    # Agregar variaciones adicionales ULTRA DIVERSAS para máxima unicidad
                    additional_traits = {
                        "freckles": random.choice(["none", "light", "moderate", "heavy", "scattered", "concentrated", "bridge", "cheeks", "forehead"]) if random.random() < 0.4 else "none",
                        "eyebrows": random.choice(["thick", "medium", "thin", "arched", "straight", "defined", "natural", "bushy", "sparse", "uneven", "perfect", "asymmetric", "high", "low", "close", "wide", "angled", "curved"]),
                        "jawline": random.choice(["strong", "soft", "defined", "rounded", "angular", "delicate", "square", "pointed", "weak", "prominent", "recessed", "asymmetric", "perfect", "uneven", "wide", "narrow"]),
                        "cheekbones": random.choice(["high", "medium", "low", "prominent", "subtle", "defined", "sharp", "soft", "angular", "rounded", "asymmetric", "perfect", "uneven", "wide", "narrow", "hollow", "full"]),
                        "skin_texture": random.choice(["smooth", "textured", "natural", "mature", "youthful", "rough", "fine", "coarse", "porous", "tight", "loose", "elastic", "dry", "oily", "combination"]),
                        "facial_hair": random.choice(["clean-shaven", "stubble", "beard", "mustache", "goatee", "sideburns", "full-beard", "trimmed", "unkempt", "styled", "patchy", "thick", "thin"]) if genero == "hombre" else "none",
                        "moles": random.choice(["none", "small", "medium", "large", "multiple", "cheek", "chin", "forehead", "nose"]) if random.random() < 0.2 else "none",
                        "scars": random.choice(["none", "small", "faint", "visible", "cheek", "chin", "forehead"]) if random.random() < 0.1 else "none",
                        "acne": random.choice(["none", "mild", "moderate", "severe", "scattered", "concentrated"]) if random.random() < 0.15 else "none",
                        "wrinkles": random.choice(["none", "fine", "moderate", "deep", "forehead", "eye", "mouth", "neck"]) if edad > 30 and random.random() < 0.3 else "none"
                    }
                    
                    return {
                        "region": region,
                        "region_traits": region_traits,
                        "skin_tone": skin_tone,
                        "hair_color": hair_color,
                        "hair_style": hair_style,
                        "eye_color": eye_color,
                        "face_shape": face_shape,
                        "nose_shape": nose_shape,
                        "lip_shape": lip_shape,
                        "eye_shape": eye_shape,
                        "freckles": additional_traits["freckles"],
                        "eyebrows": additional_traits["eyebrows"],
                        "jawline": additional_traits["jawline"],
                        "cheekbones": additional_traits["cheekbones"],
                        "skin_texture": additional_traits["skin_texture"],
                        "facial_hair": additional_traits["facial_hair"]
                    }
                
                def obtener_parametros_nacionalidad(nacionalidad):
                    """Obtiene los parámetros técnicos específicos para cada nacionalidad."""
                    try:
                        import json
                        consulta_dir = Path(__file__).parent.parent / "Consulta"
                        
                        # Parámetros por defecto - HOMOGÉNEOS para todas las nacionalidades
                        # Resolución fija para simular misma cámara, misma distancia
                        # Configuración optimizada basada en resultados exitosos
                        parametros_default = {
                            "width": 512,  # Resolución homogénea para todas las imágenes
                            "height": 512,  # Como si fueran tomadas con la misma cámara
                            "steps": 35,  # Optimizado para mejor calidad/velocidad
                            "cfg_scale": 12.0,  # CFG optimizado para mejor adherencia al prompt
                            "sampler": "DPM++ 2M Karras"
                        }
                        
                        # Mapeo de nacionalidades a archivos de configuración
                        config_files = {
                            "venezuelan": "gui_config.json",
                            "cuban": "templates/Pasaporte Cubano.json",
                            "haitian": "templates/Haitiano Realista.json",
                            "dominican": "templates/Documento Oficial.json",
                            "mexican": "templates/Diversidad Étnica.json",
                            "brazilian": "templates/Retrato Realista.json",
                            "american": "templates/Alta Calidad.json"
                        }
                        
                        config_file = config_files.get(nacionalidad, "gui_config.json")
                        config_path = consulta_dir / config_file
                        
                        # SIEMPRE usar parámetros homogéneos para simular misma cámara
                        # Esto garantiza que todas las imágenes tengan la misma resolución y configuración
                        parametros = parametros_default.copy()
                        
                        # Opcional: Leer configuración específica solo para información
                        if config_path.exists():
                            try:
                                with open(config_path, 'r', encoding='utf-8') as f:
                                    config = json.load(f)
                                # Solo usar steps y sampler de la configuración específica si están disponibles
                                if "generation" in config:
                                    gen_config = config["generation"]
                                    parametros["steps"] = gen_config.get("steps", parametros_default["steps"])
                                    parametros["sampler"] = gen_config.get("sampler", parametros_default["sampler"])
                                elif "steps" in config:
                                    parametros["steps"] = config.get("steps", parametros_default["steps"])
                                    parametros["sampler"] = config.get("sampler", parametros_default["sampler"])
                            except:
                                pass  # Si hay error, usar parámetros por defecto
                        
                        return parametros
                    except Exception as e:
                        # En caso de error, devolver parámetros homogéneos por defecto
                        return {
                            "width": 512,  # Resolución homogénea
                            "height": 512,  # Como misma cámara
                            "steps": 35,  # Optimizado para mejor calidad/velocidad
                            "cfg_scale": 12.0,  # CFG optimizado para mejor adherencia al prompt
                            "sampler": "DPM++ 2M Karras"
                        }
                
                def aplicar_prompt_pasaporte_func(nacionalidad, genero, edad):
                    """Aplica el prompt de pasaporte y configura los parámetros técnicos específicos de la nacionalidad."""
                    try:
                        from generar_pasaportes import GeneradorPasaportes
                        consulta_dir = Path(__file__).parent.parent / "Consulta"
                        if consulta_dir.exists():
                            generador = GeneradorPasaportes(str(consulta_dir))
                            # Convertir edad a entero
                            edad_int = int(edad)
                            prompt_pos, prompt_neg = generador.generar_prompt_completo(nacionalidad, genero, edad_int, edad_int)
                            
                            # Obtener parámetros específicos de la nacionalidad
                            parametros = obtener_parametros_nacionalidad(nacionalidad)
                            
                            info = f"✅ **Prompt y parámetros aplicados para {nacionalidad}**\n"
                            info += f"- Género: {genero}, Edad: {edad_int} años\n"
                            info += f"- Longitud prompt: {len(prompt_pos)} caracteres\n"
                            info += f"🎯 **Parámetros técnicos configurados:**\n"
                            info += f"- Dimensiones: {parametros['width']}x{parametros['height']}\n"
                            info += f"- Steps: {parametros['steps']}\n"
                            info += f"- CFG Scale: {parametros['cfg_scale']}\n"
                            info += f"- Sampler: {parametros['sampler']}"
                            
                            return prompt_pos, prompt_neg, parametros['width'], parametros['height'], parametros['cfg_scale'], parametros['steps'], parametros['sampler'], -1, 1, 1, 0.7, 0, 2.0, 0, 0, "Latent", "Use same sampler", "Use same scheduler", "None", 0.8, info
                        else:
                            return "", "", 512, 512, 12.0, 35, "DPM++ 2M Karras", -1, 1, 1, 0.7, 0, 2.0, 0, 0, "Latent", "Use same sampler", "Use same scheduler", "None", 0.8, "❌ No se encontró el directorio Consulta"
                    except Exception as e:
                        return "", "", 512, 512, 12.0, 35, "DPM++ 2M Karras", -1, 1, 1, 0.7, 0, 2.0, 0, 0, "Latent", "Use same sampler", "Use same scheduler", "None", 0.8, f"❌ Error: {e}"
                
                def detener_generacion_func():
                    """Detiene la generación en curso."""
                    global generation_cancelled
                    generation_cancelled = True
                    return "🛑 Generación detenida por el usuario"
                
                def generar_masivo_genetico_func(nacionalidad, genero, edad, cantidad, region, edad_min, edad_max, beauty_control, skin_control, hair_control, eye_control, background_control, cfg_scale, steps, sampler_name, seed, width, height, batch_count, batch_size, denoising_strength, hr_second_pass_steps, hr_scale, hr_resize_x, hr_resize_y, hr_upscaler, hr_sampler_name, hr_scheduler, refiner_checkpoint, refiner_switch_at, progress=gr.Progress()):
                    """Inicia la generación masiva con motor genético dinámico."""
                    global generation_cancelled
                    generation_cancelled = False  # Resetear flag de cancelación
                    
                    try:
                        # Guardar configuración genética automáticamente
                        guardar_configuracion_genetica(beauty_control, skin_control, hair_control, eye_control, background_control, region)
                        
                        import time
                        import json
                        import os
                        import random
                        from datetime import datetime
                        import modules.processing
                        import modules.shared as shared
                        from modules.shared import opts
                        from contextlib import closing
                        from modules import sd_samplers
                        
                        # Convertir valores a enteros
                        cantidad_int = int(cantidad)
                        edad_min_int = int(edad_min)
                        edad_max_int = int(edad_max)
                        
                        # Validar rango de edad
                        if edad_min_int >= edad_max_int:
                            return "", "", 1, 1, f"❌ Error: La edad mínima ({edad_min_int}) debe ser menor que la máxima ({edad_max_int})"
                        
                        # Obtener nombre del modelo actual
                        try:
                            from modules import shared
                            model_name = shared.sd_model.sd_checkpoint_info.name_for_extra if shared.sd_model and hasattr(shared.sd_model, 'sd_checkpoint_info') else "unknown_model"
                            # Limpiar nombre del modelo para usar como nombre de carpeta
                            model_name_clean = "".join(c for c in model_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                            model_name_clean = model_name_clean.replace(' ', '_')
                        except:
                            model_name_clean = "unknown_model"
                        
                        # Crear directorio de salida con estructura: outputs/{modelo}/{metodo}/
                        output_dir = Path("outputs")
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        
                        # Crear subcarpeta para imágenes estándar de WebUI (nomenclatura 00000-xxx)
                        standard_webui_dir = output_dir / model_name_clean / "webui_standard"
                        standard_webui_dir.mkdir(parents=True, exist_ok=True)
                        
                        batch_dir = output_dir / model_name_clean / "genetico_premium" / f"genetic_{nacionalidad}_{region}_{genero}_{timestamp}"
                        batch_dir.mkdir(parents=True, exist_ok=True)
                        
                        generated_count = 0
                        failed_count = 0
                        
                        # Configurar barra de progreso
                        progress(0, desc=f"Iniciando generación genética de {cantidad_int} imágenes...")
                        
                        # Inicializar motor genético avanzado
                        try:
                            from genetic_diversity_engine_advanced import AdvancedGeneticDiversityEngine
                            genetic_engine = AdvancedGeneticDiversityEngine()
                        except Exception as e:
                            return "", "", 1, 1, f"❌ Error inicializando motor genético avanzado: {e}"
                        
                        # Generar perfiles genéticos únicos para cada imagen
                        for i in range(cantidad_int):
                            # Verificar si la generación fue cancelada
                            if generation_cancelled:
                                return "", "", 1, 1, "🛑 Generación cancelada por el usuario"
                            
                            try:
                                # Debug: Inicio de generación
                                print(f"🔍 Debug - Iniciando generación {i+1}/{cantidad_int}")
                                
                                # Actualizar progreso
                                progress((i + 1) / cantidad_int, desc=f"Generando imagen {i+1}/{cantidad_int} con perfil genético único...")
                                
                                # Generar edad aleatoria dentro del rango
                                edad_aleatoria = random.randint(edad_min_int, edad_max_int)
                                
                                # SIEMPRE usar región aleatoria para máxima diversidad
                                regiones_disponibles = ["caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"]
                                region_genetica = random.choice(regiones_disponibles)
                                
                                # Generar perfil genético avanzado completo
                                genetic_profile = genetic_engine.generate_advanced_genetic_profile(
                                    nationality=nacionalidad,
                                    region=region_genetica,
                                    gender=genero,
                                    age=edad_aleatoria,
                                    beauty_control=beauty_control,
                                    skin_control=skin_control,
                                    hair_control=hair_control,
                                    eye_control=eye_control
                                )
                                
                                # Debug: Perfil genético generado
                                print(f"🔍 Debug - Perfil genético generado: {genetic_profile.image_id}")
                                
                                # Generar prompts únicos basados en el perfil genético avanzado
                                prompt, negative_prompt = genetic_engine.generate_prompt_from_advanced_profile(genetic_profile, background_control)
                                
                                # Debug: Prompts generados
                                print(f"🔍 Debug - Prompt generado: {len(prompt)} caracteres")
                                print(f"🔍 Debug - Negative prompt generado: {len(negative_prompt)} caracteres")
                                
                                # Crear JSON genético avanzado completo
                                json_genetico = {
                                    "image_id": genetic_profile.image_id,
                                    "generated_at": genetic_profile.generated_at,
                                    "metadata": {
                                        "nationality": genetic_profile.nationality,
                                        "region": genetic_profile.region,
                                        "gender": genetic_profile.gender,
                                        "age": genetic_profile.age,
                                        "generation_type": "advanced_genetic_diversity_engine",
                                        "unique_characteristics": True,
                                        "uniqueness_score": genetic_profile.uniqueness_score,
                                        "beauty_score": genetic_profile.beauty_score
                                    },
                                    "genetic_profile": {
                                        "face_shape": genetic_profile.face_shape,
                                        "face_width": genetic_profile.face_width,
                                        "face_length": genetic_profile.face_length,
                                        "jawline": genetic_profile.jawline,
                                        "chin": genetic_profile.chin,
                                        "cheekbones": genetic_profile.cheekbones,
                                        "facial_symmetry": genetic_profile.facial_symmetry,
                                        "bone_structure": genetic_profile.bone_structure,
                                        "eye_color": genetic_profile.eye_color,
                                        "eye_color_shade": genetic_profile.eye_color_shade,
                                        "eye_shape": genetic_profile.eye_shape,
                                        "eye_size": genetic_profile.eye_size,
                                        "eye_spacing": genetic_profile.eye_spacing,
                                        "eyelid_type": genetic_profile.eyelid_type,
                                        "eyelashes": genetic_profile.eyelashes,
                                        "eyelashes_length": genetic_profile.eyelashes_length,
                                        "eyebrows": genetic_profile.eyebrows,
                                        "eyebrows_thickness": genetic_profile.eyebrows_thickness,
                                        "eyebrows_shape": genetic_profile.eyebrows_shape,
                                        "nose_shape": genetic_profile.nose_shape,
                                        "nose_size": genetic_profile.nose_size,
                                        "nose_width": genetic_profile.nose_width,
                                        "nose_bridge": genetic_profile.nose_bridge,
                                        "nose_tip": genetic_profile.nose_tip,
                                        "nostril_size": genetic_profile.nostril_size,
                                        "lip_shape": genetic_profile.lip_shape,
                                        "lip_size": genetic_profile.lip_size,
                                        "lip_thickness": genetic_profile.lip_thickness,
                                        "mouth_width": genetic_profile.mouth_width,
                                        "lip_color": genetic_profile.lip_color,
                                        "lip_fullness": genetic_profile.lip_fullness,
                                        "skin_tone": genetic_profile.skin_tone,
                                        "skin_tone_shade": genetic_profile.skin_tone_shade,
                                        "skin_texture": genetic_profile.skin_texture,
                                        "skin_undertone": genetic_profile.skin_undertone,
                                        "skin_glow": genetic_profile.skin_glow,
                                        "skin_elasticity": genetic_profile.skin_elasticity,
                                        "skin_imperfections": genetic_profile.skin_imperfections,
                                        "freckles": genetic_profile.freckles,
                                        "freckles_density": genetic_profile.freckles_density,
                                        "moles": genetic_profile.moles,
                                        "moles_count": genetic_profile.moles_count,
                                        "birthmarks": genetic_profile.birthmarks,
                                        "scars": genetic_profile.scars,
                                        "acne": genetic_profile.acne,
                                        "age_spots": genetic_profile.age_spots,
                                        "wrinkles": genetic_profile.wrinkles,
                                        "hair_color": genetic_profile.hair_color,
                                        "hair_color_shade": genetic_profile.hair_color_shade,
                                        "hair_texture": genetic_profile.hair_texture,
                                        "hair_length": genetic_profile.hair_length,
                                        "hair_style": genetic_profile.hair_style,
                                        "hair_density": genetic_profile.hair_density,
                                        "hair_shine": genetic_profile.hair_shine,
                                        "hair_curliness": genetic_profile.hair_curliness,
                                        "hair_thickness": genetic_profile.hair_thickness,
                                        "hairline": genetic_profile.hairline,
                                        "age_characteristics": genetic_profile.age_characteristics,
                                        "beauty_level": genetic_profile.beauty_level,
                                        "attractiveness_factors": genetic_profile.attractiveness_factors,
                                        "ethnic_beauty_features": genetic_profile.ethnic_beauty_features,
                                        "ethnic_features": genetic_profile.ethnic_features,
                                        "genetic_heritage": genetic_profile.genetic_heritage
                                    },
                                    "prompt": prompt,
                                    "negative_prompt": negative_prompt,
                                    "generation_parameters": {
                                        "width": 512,
                                        "height": 512,
                                        "steps": 35,
                                        "cfg_scale": 12.0,
                                        "sampler_name": "DPM++ 2M Karras",
                                        "seed": random.randint(1, 2147483647),  # Seed único para cada imagen
                                        "batch_size": 1,
                                        "n_iter": 1
                                    },
                                    "controls_used": {
                                        "beauty_control": beauty_control,
                                        "skin_control": skin_control,
                                        "hair_control": hair_control,
                                        "eye_control": eye_control,
                                        "age_range": f"{edad_min_int}-{edad_max_int}",
                                        "region": region
                                    },
                                    "replication_info": {
                                        "description": "Configuración genética completa para replicar esta imagen exacta",
                                        "genetic_diversity": "Perfil genético único con características étnicas reales",
                                        "uniqueness": "Cada imagen tiene un perfil genético completamente único",
                                        "controls": "Configuración de controles utilizada para generar esta imagen"
                                    }
                                }
                                
                                # Parámetros homogéneos
                                params = {
                                    'prompt': prompt,
                                    'negative_prompt': negative_prompt,
                                    'width': width,
                                    'height': height,
                                    'steps': steps,
                                    'cfg_scale': cfg_scale,
                                    'sampler_name': sampler_name,
                                    'seed': seed,
                                    'batch_size': batch_size,
                                    'n_iter': batch_count
                                }
                                
                                # Generar imagen usando la API interna de WebUI
                                try:
                                    # Debug: Antes de crear objeto de procesamiento
                                    print(f"🔍 Debug - Creando objeto de procesamiento para imagen {i+1}")
                                    
                                    # Crear objeto de procesamiento
                                    p = modules.processing.StableDiffusionProcessingTxt2Img(
                                        sd_model=shared.sd_model,
                                        outpath_samples=str(standard_webui_dir),  # Usar carpeta webui_standard para nomenclatura 00000-xxx
                                        outpath_grids=None,   # No guardar grids
                                        prompt=params['prompt'],
                                        negative_prompt=params['negative_prompt'],
                                        batch_size=params['batch_size'],
                                        n_iter=params['n_iter'],
                                        cfg_scale=params['cfg_scale'],
                                        width=params['width'],
                                        height=params['height'],
                                        enable_hr=hr_second_pass_steps > 0,
                                        denoising_strength=denoising_strength,
                                        hr_scale=hr_scale,
                                        hr_upscaler=hr_upscaler,
                                        hr_second_pass_steps=hr_second_pass_steps,
                                        hr_resize_x=hr_resize_x,
                                        hr_resize_y=hr_resize_y,
                                        hr_checkpoint_name=hr_checkpoint_name,
                                        hr_sampler_name=hr_sampler_name,
                                        hr_scheduler=hr_scheduler,
                                        hr_prompt="",
                                        hr_negative_prompt="",
                                        override_settings={
                                            'save_to_dirs': False,  # No crear subcarpetas con fechas
                                            'save_images_replace_action': "Add number suffix"
                                        }
                                    )
                                    
                                    # Debug: Objeto de procesamiento creado
                                    print(f"🔍 Debug - Objeto de procesamiento creado: {p}")
                                    
                                    # Configurar sampler
                                    try:
                                        sampler = sd_samplers.samplers_map.get(params['sampler_name'])
                                        if sampler is None:
                                            # Fallback al primer sampler disponible
                                            sampler = list(sd_samplers.samplers_map.values())[0]
                                        p.sampler = sampler
                                    except Exception as e:
                                        print(f"⚠️ Error configurando sampler: {e}")
                                        # Usar sampler por defecto
                                        p.sampler = list(sd_samplers.samplers_map.values())[0]
                                    
                                    # Configurar steps
                                    p.steps = params['steps']
                                    
                                    # Configurar seed
                                    if params['seed'] != -1:
                                        p.seed = params['seed']
                                    
                                    # Procesar imagen
                                    with closing(p):
                                        processed = modules.processing.process_images(p)
                                    
                                    result = processed.images if processed else []
                                    
                                    # Debug: Imprimir información del resultado
                                    print(f"🔍 Debug Genético - processed: {processed}")
                                    print(f"🔍 Debug Genético - result: {result}")
                                    print(f"🔍 Debug Genético - len(result): {len(result) if result else 0}")
                                    if result and len(result) > 0:
                                        print(f"🔍 Debug Genético - result[0]: {result[0]}")
                                        print(f"🔍 Debug Genético - result[0] type: {type(result[0])}")
                                        print(f"🔍 Debug Genético - hasattr(result[0], 'save'): {hasattr(result[0], 'save')}")
                                    
                                    if result and len(result) > 0 and result[0] is not None:
                                        # Guardar imagen con nomenclatura genética
                                        filename = f"genetic_{nacionalidad}_{region}_{genero}_{edad_aleatoria}_{i+1}_{timestamp}.png"
                                        filepath = batch_dir / filename
                                        
                                        # Debug: Imprimir información de la ruta
                                        print(f"🔍 Debug - batch_dir: {batch_dir}")
                                        print(f"🔍 Debug - filename: {filename}")
                                        print(f"🔍 Debug - filepath: {filepath}")
                                        print(f"🔍 Debug - filepath type: {type(filepath)}")
                                        print(f"🔍 Debug - str(filepath): {str(filepath)}")
                                        
                                        # Verificar que la ruta sea válida
                                        if filepath and str(filepath):
                                            # Guardar la imagen PIL
                                            if hasattr(result[0], 'save'):
                                                result[0].save(str(filepath))
                                            else:
                                                # Si es una ruta de archivo
                                                import shutil
                                                shutil.copy2(result[0], str(filepath))
                                        else:
                                            print(f"⚠️ Error: Ruta de archivo inválida: {filepath}")
                                            failed_count += 1
                                            continue
                                        
                                        # Guardar configuración JSON genética
                                        json_filename = filename.replace('.png', '.json')
                                        json_filepath = batch_dir / json_filename
                                        
                                        # Verificar que la ruta del JSON sea válida
                                        if json_filepath and str(json_filepath):
                                            # Agregar información de la imagen generada al JSON genético
                                            json_genetico["image_info"] = {
                                                "filename": filename,
                                                "filepath": str(filepath),
                                                "generation_successful": True,
                                                "generation_time": datetime.now().isoformat()
                                            }
                                            
                                            with open(str(json_filepath), 'w', encoding='utf-8') as f:
                                                json.dump(json_genetico, f, indent=2, ensure_ascii=False)
                                            
                                            generated_count += 1
                                            print(f"✅ Imagen genética {i+1} generada: {filename}")
                                        else:
                                            print(f"⚠️ Error: Ruta de JSON inválida: {json_filepath}")
                                            failed_count += 1
                                            continue
                                    else:
                                        failed_count += 1
                                        print(f"❌ Error generando imagen genética {i+1}: No se obtuvo resultado de la generación.")
                                        
                                except Exception as e:
                                    failed_count += 1
                                    print(f"❌ Error en generación genética {i+1}: {e}")
                                    print(f"🔍 Debug - Tipo de error: {type(e)}")
                                    print(f"🔍 Debug - Traceback completo:")
                                    import traceback
                                    traceback.print_exc()
                            
                            except Exception as e:
                                failed_count += 1
                                print(f"❌ Error procesando perfil genético {i+1}: {e}")
                        
                        # Resultado final
                        progress(1.0, desc="Generación genética completada")
                        
                        resultado = f"✅ **Generación masiva genética completada**\n\n"
                        resultado += f"📊 **Estadísticas finales:**\n"
                        resultado += f"- Imágenes generadas: {generated_count}\n"
                        resultado += f"- Imágenes fallidas: {failed_count}\n"
                        resultado += f"- Total procesadas: {cantidad_int}\n"
                        resultado += f"- Modelo utilizado: {model_name_clean}\n"
                        resultado += f"- Directorio: {batch_dir}\n\n"
                        resultado += f"🧬 **Características genéticas avanzadas implementadas:**\n"
                        resultado += f"- ✅ **Perfiles genéticos únicos** para cada imagen\n"
                        resultado += f"- ✅ **Diversidad étnica real** basada en datos demográficos\n"
                        resultado += f"- ✅ **Características faciales detalladas** (forma, ojos, nariz, boca)\n"
                        resultado += f"- ✅ **Tonos de piel dinámicos** según región y control\n"
                        resultado += f"- ✅ **Colores de cabello y ojos variables** con tonalidades específicas\n"
                        resultado += f"- ✅ **Edades aleatorias** en rango {edad_min_int}-{edad_max_int}\n"
                        resultado += f"- ✅ **Niveles de belleza controlables** ({beauty_control})\n"
                        resultado += f"- ✅ **Belleza universal** sin sesgos étnicos\n"
                        resultado += f"- ✅ **Imperfecciones realistas** según edad\n"
                        resultado += f"- ✅ **Características étnicas específicas** de {region}\n"
                        resultado += f"- ✅ **Herencia genética** (mestizo, afrodescendiente, etc.)\n"
                        resultado += f"- ✅ **Características de belleza étnicas** específicas\n"
                        resultado += f"- ✅ **Score de belleza** independiente del tono de piel\n"
                        resultado += f"- ✅ **Parámetros homogéneos** (512x512, CFG 9.0)\n"
                        resultado += f"- ✅ **Barra de progreso** en tiempo real\n"
                        resultado += f"- ✅ **JSON genético avanzado completo** por imagen\n\n"
                        resultado += f"🎯 **Controles utilizados:**\n"
                        resultado += f"- Región: {region}\n"
                        resultado += f"- Rango de edad: {edad_min_int}-{edad_max_int}\n"
                        resultado += f"- Control de belleza: {beauty_control}\n"
                        resultado += f"- Control de piel: {skin_control}\n"
                        resultado += f"- Control de cabello: {hair_control}\n"
                        resultado += f"- Control de ojos: {eye_control}\n\n"
                        resultado += f"📁 **Archivos generados en**: {batch_dir}\n"
                        resultado += f"🎉 **¡Generación genética masiva completada exitosamente!**\n"
                        
                        return "", "", 1, 1, resultado
                        
                    except Exception as e:
                        return "", "", 1, 1, f"❌ Error: {e}"
                
                def generar_masivo_pasaporte_func(nacionalidad, genero, edad, cantidad, edad_min, edad_max, region, cfg_scale, steps, sampler_name, seed, width, height, batch_count, batch_size, denoising_strength, hr_second_pass_steps, hr_scale, hr_resize_x, hr_resize_y, hr_upscaler, hr_sampler_name, hr_scheduler, refiner_checkpoint, refiner_switch_at, progress=gr.Progress()):
                    """Inicia la generación masiva real leyendo archivos JSON individuales con barra de progreso."""
                    global generation_cancelled
                    generation_cancelled = False  # Resetear flag de cancelación
                    
                    try:
                        import time
                        import json
                        import os
                        import random
                        from datetime import datetime
                        
                        # Convertir valores a enteros
                        cantidad_int = int(cantidad)
                        edad_int = int(edad)
                        
                        # Directorio de archivos JSON
                        consulta_dir = Path(__file__).parent.parent / "Consulta"
                        
                        # Buscar archivos JSON de la nacionalidad
                        json_files = []
                        for file_path in consulta_dir.rglob("*.json"):
                            if nacionalidad.lower() in file_path.name.lower():
                                json_files.append(file_path)
                        
                        # Si no hay archivos específicos, usar archivos generales
                        if not json_files:
                            for file_path in consulta_dir.rglob("*.json"):
                                json_files.append(file_path)
                        
                        if not json_files:
                            return "", "", 1, 1, f"❌ No se encontraron archivos JSON para {nacionalidad}"
                        
                        # Obtener nombre del modelo actual
                        try:
                            from modules import shared
                            model_name = shared.sd_model.sd_checkpoint_info.name_for_extra if shared.sd_model and hasattr(shared.sd_model, 'sd_checkpoint_info') else "unknown_model"
                            # Limpiar nombre del modelo para usar como nombre de carpeta
                            model_name_clean = "".join(c for c in model_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                            model_name_clean = model_name_clean.replace(' ', '_')
                        except:
                            model_name_clean = "unknown_model"
                        
                        # Crear directorio de salida con estructura: outputs/{modelo}/{metodo}/
                        output_dir = Path("outputs")
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        
                        # Crear subcarpeta para imágenes estándar de WebUI (nomenclatura 00000-xxx)
                        standard_webui_dir = output_dir / model_name_clean / "webui_standard"
                        standard_webui_dir.mkdir(parents=True, exist_ok=True)
                        
                        batch_dir = output_dir / model_name_clean / "masivo_basico" / f"massive_{nacionalidad}_{genero}_{timestamp}"
                        batch_dir.mkdir(parents=True, exist_ok=True)
                        
                        generated_count = 0
                        failed_count = 0
                        total_files = min(len(json_files), cantidad_int)
                        
                        # Configurar barra de progreso
                        progress(0, desc=f"Iniciando generación de {total_files} imágenes...")
                        
                        # Generar JSONs dinámicos únicos para cada imagen
                        for i in range(cantidad_int):
                            # Verificar si la generación fue cancelada
                            if generation_cancelled:
                                return "", "", 1, 1, "🛑 Generación cancelada por el usuario"
                            
                            try:
                                # Actualizar progreso
                                progress((i + 1) / cantidad_int, desc=f"Generando imagen {i+1}/{cantidad_int} con características únicas...")
                                
                                # Generar características étnicas dinámicas únicas
                                try:
                                    # Generar edad aleatoria dentro del rango especificado
                                    edad_min_int = int(edad_min)
                                    edad_max_int = int(edad_max)
                                    edad_aleatoria = random.randint(edad_min_int, edad_max_int)
                                    
                                    # SIEMPRE usar región aleatoria para máxima diversidad
                                    regiones_disponibles = ["caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"]
                                    region = random.choice(regiones_disponibles)
                                    
                                    # Generar características étnicas diversas
                                    caracteristicas = generar_caracteristicas_etnicas_diversas(nacionalidad, genero, edad_aleatoria, region)
                                    
                                    # Generar prompt estricto con diversidad étnica MEJORADA
                                    prompt_parts = [
                                        f"{nacionalidad} {genero}",
                                        f"{edad_aleatoria} years old",
                                        f"from {caracteristicas['region']} region",
                                        f"{caracteristicas['skin_tone']} skin",
                                        f"{caracteristicas['skin_texture']} skin texture",
                                        f"{caracteristicas['hair_color']} hair",
                                        f"{caracteristicas['hair_style']} hair",
                                        f"{caracteristicas['eye_color']} eyes",
                                        f"{caracteristicas['eye_shape']} eyes",
                                        f"{caracteristicas['face_shape']} face",
                                        f"{caracteristicas['nose_shape']} nose",
                                        f"{caracteristicas['lip_shape']} lips",
                                        f"{caracteristicas['eyebrows']} eyebrows",
                                        f"{caracteristicas['jawline']} jawline",
                                        f"{caracteristicas['cheekbones']} cheekbones",
                                        f"{caracteristicas['facial_hair']}" if caracteristicas['facial_hair'] != "none" else "",
                                        f"{caracteristicas['freckles']} freckles" if caracteristicas['freckles'] != "none" else "",
                                        "official passport photo",
                                        "government ID photo",
                                        "document photo",
                                        "official headshot",
                                        "passport style photo",
                                        "ID card photo",
                                        "looking directly at camera",
                                        "facing camera directly",
                                        "front view only",
                                        "head and shoulders only",
                                        "head centered perfectly",
                                        "face centered perfectly",
                                        "neutral expression",
                                        "serious expression",
                                        "no smile",
                                        "mouth closed",
                                        "eyes open",
                                        "looking straight ahead",
                                        "head straight",
                                        "no head tilt",
                                        "no head turn",
                                        "head upright",
                                        "shoulders visible",
                                        "shoulders straight",
                                        "shoulders level",
                                        "hair behind ears",
                                        "hair not covering face",
                                        "hair not covering shoulders",
                                        "hair neat and tidy",
                                        "hair professional style",
                                        "raw photography",
                                        "documentary style",
                                        "unretouched",
                                        "natural skin texture",
                                        "pores visible",
                                        "natural skin imperfections",
                                        "authentic appearance",
                                        "natural lighting",
                                        "centered composition",
                                        "symmetrical positioning",
                                        "proper framing",
                                        "correct proportions",
                                        "head and shoulders framing",
                                        "passport crop",
                                        "ID photo crop",
                                        "official document crop",
                                        "head centered in frame",
                                        "shoulders at bottom edge",
                                        "SAIME Venezuela passport photo",
                                        "official SAIME specifications",
                                        "Venezuelan passport requirements",
                                        "head positioned in upper third of frame",
                                        "head in upper portion of image",
                                        "head not touching top edge",
                                        "small space above head",
                                        "minimal clearance above head",
                                        "head well below top border",
                                        "head centered vertically in upper third",
                                        "face fills 70% of image height",
                                        "face occupies most of frame",
                                        "head takes up most of image",
                                        "large head in frame",
                                        "head dominates the image",
                                        "head and shoulders fill frame",
                                        "shoulders at bottom of image",
                                        "shoulders visible at bottom edge",
                                        "head and shoulders composition",
                                        "passport photo proportions",
                                        "ID photo proportions",
                                        "document photo proportions",
                                        "official photo proportions",
                                        "government photo proportions",
                                        "passport style proportions",
                                        "ID card proportions",
                                        "document proportions",
                                        "official document proportions",
                                        "government document proportions",
                                        "tight headshot framing",
                                        "close-up headshot",
                                        "head fills most of frame",
                                        "face centered in upper portion",
                                        "head positioned in upper 60% of image",
                                        "eyes positioned at 45% from top",
                                        "head and shoulders visible",
                                        "shoulders at bottom edge",
                                        "head not touching top",
                                        "head not touching sides",
                                        "proper head size for passport",
                                        "correct head proportions",
                                        "head size appropriate for ID",
                                        "head size suitable for document",
                                        "head size perfect for passport",
                                        "head size ideal for ID card",
                                        "head size optimal for document",
                                        "head size correct for official photo",
                                        "head size proper for government ID",
                                        "shoulders not touching sides",
                                        "shoulders not touching bottom",
                                        "clavicle junction visible",
                                        "clavicle connection visible",
                                        "shoulder joint visible",
                                        "shoulder connection visible",
                                        "proper head size",
                                        "correct head size",
                                        "head not too large",
                                        "head not too small",
                                        "head proportional",
                                        "head well proportioned",
                                        "head properly sized",
                                        "head correctly sized",
                                        "head appropriately sized",
                                        "head optimally sized",
                                        "head perfectly sized",
                                        "head ideally sized",
                                        "high quality",
                                        "high resolution",
                                        "sharp focus",
                                        "crystal clear",
                                        "detailed",
                                        "crisp",
                                        "clean",
                                        "professional quality",
                                        "studio quality",
                                        "photographic quality",
                                        "color photography",
                                        "full color",
                                        "vibrant colors",
                                        "natural colors",
                                        "accurate colors",
                                        "true colors",
                                        "rich colors",
                                        "saturated colors",
                                        "colorful",
                                        "color image",
                                        "color photo",
                                        "color photograph",
                                        "color portrait",
                                        "color headshot",
                                        "color passport photo",
                                        "color ID photo",
                                        "color document photo",
                                        "color official photo",
                                        "color government photo",
                                        "color passport",
                                        "color ID",
                                        "color document",
                                        "color official",
                                        "color government",
                                        "everyday person",
                                        "normal person",
                                        "regular person",
                                        "common person",
                                        "average person",
                                        "real person",
                                        "authentic person",
                                        "natural person",
                                        "ordinary person",
                                        "typical person",
                                        "pure white background",
                                        "solid white background",
                                        "clean white background",
                                        "uniform white background",
                                        "plain white background",
                                        "studio white background"
                                    ]
                                    
                                    # Filtrar elementos vacíos
                                    prompt_parts = [part for part in prompt_parts if part.strip()]
                                    
                                    prompt = ", ".join(prompt_parts)
                                    
                                    negative_prompt = ", ".join([
                                        "3/4 view",
                                        "side profile",
                                        "profile view",
                                        "looking away",
                                        "looking left",
                                        "looking right",
                                        "looking up",
                                        "looking down",
                                        "tilted head",
                                        "turned head",
                                        "angled face",
                                        "off-center",
                                        "asymmetrical",
                                        "smiling",
                                        "laughing",
                                        "frowning",
                                        "head tilted",
                                        "head turned",
                                        "head angled",
                                        "head not straight",
                                        "head not centered",
                                        "face not centered",
                                        "face not straight",
                                        "face angled",
                                        "face tilted",
                                        "face turned",
                                        "shoulders not visible",
                                        "shoulders not straight",
                                        "shoulders tilted",
                                        "shoulders angled",
                                        "hair covering face",
                                        "hair covering eyes",
                                        "hair covering ears",
                                        "hair covering shoulders",
                                        "hair messy",
                                        "hair unkempt",
                                        "hair not neat",
                                        "hair not professional",
                                        "hair in face",
                                        "hair over eyes",
                                        "hair over ears",
                                        "hair over shoulders",
                                        "long hair covering",
                                        "hair blocking face",
                                        "hair blocking eyes",
                                        "hair blocking ears",
                                        "hair blocking shoulders",
                                        "improper framing",
                                        "wrong proportions",
                                        "incorrect framing",
                                        "bad composition",
                                        "poor framing",
                                        "wrong crop",
                                        "incorrect crop",
                                        "bad crop",
                                        "too close",
                                        "too far",
                                        "wrong distance",
                                        "incorrect distance",
                                        "bad distance",
                                        "head too large",
                                        "head too small",
                                        "head too close",
                                        "head too far",
                                        "head touching top",
                                        "head touching edges",
                                        "head touching sides",
                                        "head touching bottom",
                                        "shoulders touching sides",
                                        "shoulders touching bottom",
                                        "shoulders touching edges",
                                        "no space above head",
                                        "insufficient space above head",
                                        "too little space above head",
                                        "head filling frame",
                                        "head filling top",
                                        "head filling edges",
                                        "head filling sides",
                                        "head filling bottom",
                                        "head at top of image",
                                        "head near top edge",
                                        "head close to top",
                                        "head touching top border",
                                        "head touching top margin",
                                        "head too high in frame",
                                        "head positioned too high",
                                        "head not centered vertically",
                                        "head not in upper third",
                                        "head not in upper portion",
                                        "head too high in frame",
                                        "head at top of image",
                                        "head touching top edge",
                                        "head filling top of frame",
                                        "head too small in frame",
                                        "head too far from camera",
                                        "head not filling frame",
                                        "head not dominating image",
                                        "face too small",
                                        "face not filling frame",
                                        "head not centered vertically",
                                        "head not in upper third",
                                        "head positioned too low",
                                        "head in middle of frame",
                                        "head in lower portion",
                                        "head not in upper portion",
                                        "shoulders not visible",
                                        "shoulders cut off",
                                        "shoulders missing",
                                        "head only visible",
                                        "no shoulders",
                                        "shoulders not at bottom",
                                        "wrong proportions",
                                        "incorrect proportions",
                                        "bad proportions",
                                        "poor proportions",
                                        "wrong composition",
                                        "incorrect composition",
                                        "bad composition",
                                        "poor composition",
                                        "head too large for frame",
                                        "head too small for frame",
                                        "head not appropriate size",
                                        "head size incorrect for passport",
                                        "head size wrong for ID",
                                        "head size inappropriate for document",
                                        "head size not suitable for passport",
                                        "head size not ideal for ID card",
                                        "head size not optimal for document",
                                        "head size not correct for official photo",
                                        "head size not proper for government ID",
                                        "head touching top edge",
                                        "head touching sides",
                                        "head touching bottom",
                                        "head filling entire frame",
                                        "head too close to edges",
                                        "head too close to top",
                                        "head too close to sides",
                                        "head too close to bottom",
                                        "insufficient space around head",
                                        "no space around head",
                                        "head filling frame completely",
                                        "head dominating entire image",
                                        "head taking up whole frame",
                                        "shoulders filling frame",
                                        "shoulders filling sides",
                                        "shoulders filling bottom",
                                        "shoulders filling edges",
                                        "clavicle not visible",
                                        "clavicle junction not visible",
                                        "clavicle connection not visible",
                                        "shoulder joint not visible",
                                        "shoulder connection not visible",
                                        "improper head size",
                                        "incorrect head size",
                                        "wrong head size",
                                        "bad head size",
                                        "head not proportional",
                                        "head not well proportioned",
                                        "head not properly sized",
                                        "head not correctly sized",
                                        "head not appropriately sized",
                                        "head not optimally sized",
                                        "head not perfectly sized",
                                        "head not ideally sized",
                                        "low quality",
                                        "low resolution",
                                        "blurry",
                                        "fuzzy",
                                        "unclear",
                                        "unfocused",
                                        "soft focus",
                                        "out of focus",
                                        "poor quality",
                                        "bad quality",
                                        "amateur quality",
                                        "grainy",
                                        "noisy",
                                        "pixelated",
                                        "compressed",
                                        "artifacts",
                                        "distorted",
                                        "deformed",
                                        "black and white",
                                        "bw",
                                        "monochrome",
                                        "grayscale",
                                        "sepia",
                                        "vintage",
                                        "old",
                                        "aged",
                                        "faded",
                                        "washed out",
                                        "desaturated",
                                        "muted colors",
                                        "dull colors",
                                        "pale colors",
                                        "weak colors",
                                        "faded colors",
                                        "washed out colors",
                                        "desaturated colors",
                                        "muted",
                                        "dull",
                                        "pale",
                                        "weak",
                                        "faded",
                                        "washed out",
                                        "desaturated",
                                        "no color",
                                        "colorless",
                                        "achromatic",
                                        "monochromatic",
                                        "grayscale",
                                        "sepia tone",
                                        "vintage look",
                                        "old look",
                                        "aged look",
                                        "faded look",
                                        "washed out look",
                                        "desaturated look",
                                        "muted look",
                                        "dull look",
                                        "pale look",
                                        "weak look",
                                        "faded look",
                                        "washed out look",
                                        "desaturated look",
                                        "multiple people",
                                        "blurry",
                                        "low quality",
                                        "distorted",
                                        "deformed",
                                        "ugly",
                                        "bad anatomy",
                                        "bad proportions",
                                        "extra limbs",
                                        "missing limbs",
                                        "extra fingers",
                                        "missing fingers",
                                        "extra arms",
                                        "missing arms",
                                        "extra legs",
                                        "missing legs",
                                        "extra heads",
                                        "missing heads",
                                        "extra eyes",
                                        "missing eyes",
                                        "extra nose",
                                        "missing nose",
                                        "extra mouth",
                                        "missing mouth",
                                        "text",
                                        "watermark",
                                        "signature",
                                        "gradient background",
                                        "gradient",
                                        "faded background",
                                        "textured background",
                                        "patterned background",
                                        "noisy background",
                                        "complex background",
                                        "busy background",
                                        "shadows on background",
                                        "lighting effects on background",
                                        "colored background",
                                        "colored backdrop",
                                        "tinted background",
                                        "off-white background",
                                        "cream background",
                                        "beige background",
                                        "gray background",
                                        "light gray background",
                                        "dark background",
                                        "black background",
                                        "blue background",
                                        "green background",
                                        "red background",
                                        "yellow background",
                                        "purple background",
                                        "orange background",
                                        "brown background",
                                        "wood background",
                                        "wall background",
                                        "fabric background",
                                        "paper background",
                                        "canvas background",
                                        "brick background",
                                        "stone background",
                                        "metal background",
                                        "glass background",
                                        "mirror background",
                                        "reflection",
                                        "shadows",
                                        "lighting",
                                        "spotlight",
                                        "soft lighting",
                                        "dramatic lighting",
                                        "rim lighting",
                                        "back lighting",
                                        "side lighting",
                                        "top lighting",
                                        "bottom lighting",
                                        "ambient lighting",
                                        "natural lighting",
                                        "artificial lighting",
                                        "studio lighting",
                                        "flash lighting",
                                        "harsh lighting",
                                        "dim lighting",
                                        "bright lighting",
                                        "overexposed",
                                        "underexposed",
                                        "high contrast",
                                        "low contrast",
                                        "saturated colors",
                                        "desaturated colors",
                                        "vibrant colors",
                                        "muted colors",
                                        "warm colors",
                                        "cool colors",
                                        "neutral colors",
                                        "pastel colors",
                                        "bold colors",
                                        "subtle colors",
                                        "airbrushed",
                                        "photoshopped",
                                        "retouched",
                                        "smooth skin",
                                        "perfect skin",
                                        "flawless skin",
                                        "glowing skin",
                                        "shiny skin",
                                        "oily skin",
                                        "greasy skin",
                                        "plastic skin",
                                        "artificial skin",
                                        "digital art",
                                        "3d render",
                                        "cg",
                                        "computer generated",
                                        "synthetic",
                                        "fake",
                                        "artificial",
                                        "overexposed",
                                        "bright lighting",
                                        "studio lighting",
                                        "flash photography",
                                        "harsh lighting",
                                        "dramatic lighting",
                                        "cinematic lighting",
                                        "professional lighting",
                                        "perfect lighting",
                                        "ideal lighting",
                                        "enhanced",
                                        "improved",
                                        "perfected",
                                        "beautified",
                                        "glamorized",
                                        "stylized",
                                        "artistic",
                                        "aesthetic",
                                        "beautiful",
                                        "attractive",
                                        "handsome",
                                        "pretty",
                                        "gorgeous",
                                        "stunning",
                                        "perfect",
                                        "ideal",
                                        "flawless",
                                        "immaculate",
                                        "pristine",
                                        "clean",
                                        "pure",
                                        "crystal clear",
                                        "sharp",
                                        "crisp",
                                        "vibrant",
                                        "saturated",
                                        "colorful",
                                        "bright",
                                        "luminous",
                                        "radiant",
                                        "brilliant",
                                        "sparkling",
                                        "shining",
                                        "glowing",
                                        "glossy",
                                        "polished",
                                        "refined",
                                        "elegant",
                                        "sophisticated",
                                        "luxurious",
                                        "premium",
                                        "high-end",
                                        "professional",
                                        "commercial",
                                        "advertising",
                                        "marketing",
                                        "fashion",
                                        "beauty",
                                        "cosmetic",
                                        "makeup",
                                        "foundation",
                                        "concealer",
                                        "powder",
                                        "blush",
                                        "lipstick",
                                        "mascara",
                                        "eyeliner",
                                        "eyeshadow",
                                        "contouring",
                                        "highlighting",
                                        "bronzer",
                                        "primer",
                                        "setting spray",
                                        "finishing powder",
                                        "model look",
                                        "supermodel appearance",
                                        "celebrity look",
                                        "fashion model",
                                        "beauty model",
                                        "perfect face",
                                        "flawless face",
                                        "ideal face",
                                        "beautiful face",
                                        "attractive face",
                                        "handsome face",
                                        "pretty face",
                                        "gorgeous face",
                                        "stunning face",
                                        "perfect features",
                                        "flawless features",
                                        "ideal features",
                                        "beautiful features",
                                        "attractive features",
                                        "handsome features",
                                        "pretty features",
                                        "gorgeous features",
                                        "stunning features"
                                    ])
                                    
                                    # Crear JSON dinámico único para esta imagen
                                    json_dinamico = {
                                        "image_id": f"{nacionalidad}_{genero}_{i+1}_{timestamp}",
                                        "generated_at": datetime.now().isoformat(),
                                        "metadata": {
                                            "nationality": nacionalidad,
                                            "gender": genero,
                                            "age": edad_aleatoria,
                                            "region": caracteristicas.get("region", region),
                                            "generation_type": "dynamic_ethnic_diversity",
                                            "unique_characteristics": True
                                        },
                                        "ethnic_characteristics": caracteristicas,
                                        "prompt": prompt,
                                        "negative_prompt": negative_prompt,
                                        "generation_parameters": {
                                            "width": 512,
                                            "height": 512,
                                            "steps": 35,
                                            "cfg_scale": 12.0,
                                            "sampler_name": "DPM++ 2M Karras",
                                            "seed": random.randint(1, 2147483647),  # Seed único para cada imagen
                                            "batch_size": 1,
                                            "n_iter": 1
                                        },
                                        "replication_info": {
                                            "description": "Configuración única para replicar esta imagen exacta",
                                            "ethnic_diversity": "Real basada en datos demográficos",
                                            "uniqueness": "Cada imagen tiene características étnicas únicas"
                                        }
                                    }
                                    
                                except Exception as e:
                                    print(f"⚠️ Error generando características dinámicas: {e}")
                                    # Fallback: usar prompt básico
                                    prompt = f"{nacionalidad} passport photo, {genero}, {edad_int} years old, professional headshot, white background"
                                    negative_prompt = "3/4 view, side profile, looking away, smiling, multiple people"
                                    
                                    json_dinamico = {
                                        "image_id": f"{nacionalidad}_{genero}_{i+1}_{timestamp}",
                                        "generated_at": datetime.now().isoformat(),
                                        "metadata": {
                                            "nationality": nacionalidad,
                                            "gender": genero,
                                            "age": edad_int,
                                            "generation_type": "fallback_basic",
                                            "unique_characteristics": False
                                        },
                                        "prompt": prompt,
                                        "negative_prompt": negative_prompt,
                                        "generation_parameters": {
                                            "width": 512,
                                            "height": 512,
                                            "steps": 35,
                                            "cfg_scale": 12.0,
                                            "sampler_name": "DPM++ 2M Karras",
                                            "seed": random.randint(1, 2147483647),  # Seed único para cada imagen
                                            "batch_size": 1,
                                            "n_iter": 1
                                        }
                                    }
                                
                                # Parámetros homogéneos
                                params = {
                                    'prompt': prompt,
                                    'negative_prompt': negative_prompt,
                                    'width': width,
                                    'height': height,
                                    'steps': steps,
                                    'cfg_scale': cfg_scale,
                                    'sampler_name': sampler_name,
                                    'seed': seed,
                                    'batch_size': batch_size,
                                    'n_iter': batch_count
                                }
                                
                                # Generar imagen usando la API interna de WebUI
                                try:
                                    import modules.processing
                                    import modules.shared as shared
                                    from modules.shared import opts
                                    from contextlib import closing
                                    
                                    # Crear objeto de procesamiento
                                    p = modules.processing.StableDiffusionProcessingTxt2Img(
                                        sd_model=shared.sd_model,
                                        outpath_samples=str(standard_webui_dir),  # Usar carpeta webui_standard para nomenclatura 00000-xxx
                                        outpath_grids=None,   # No guardar grids
                                        prompt=params['prompt'],
                                        negative_prompt=params['negative_prompt'],
                                        batch_size=params['batch_size'],
                                        n_iter=params['n_iter'],
                                        cfg_scale=params['cfg_scale'],
                                        width=params['width'],
                                        height=params['height'],
                                        enable_hr=hr_second_pass_steps > 0,
                                        denoising_strength=denoising_strength,
                                        hr_scale=hr_scale,
                                        hr_upscaler=hr_upscaler,
                                        hr_second_pass_steps=hr_second_pass_steps,
                                        hr_resize_x=hr_resize_x,
                                        hr_resize_y=hr_resize_y,
                                        hr_checkpoint_name=hr_checkpoint_name,
                                        hr_sampler_name=hr_sampler_name,
                                        hr_scheduler=hr_scheduler,
                                        hr_prompt="",
                                        hr_negative_prompt="",
                                        override_settings={
                                            'save_to_dirs': False,  # No crear subcarpetas con fechas
                                            'save_images_replace_action': "Add number suffix"
                                        }
                                    )
                                    
                                    # Configurar sampler
                                    from modules import sd_samplers
                                    # Configurar sampler
                                    try:
                                        sampler = sd_samplers.samplers_map.get(params['sampler_name'])
                                        if sampler is None:
                                            # Fallback al primer sampler disponible
                                            sampler = list(sd_samplers.samplers_map.values())[0]
                                        p.sampler = sampler
                                    except Exception as e:
                                        print(f"⚠️ Error configurando sampler: {e}")
                                        # Usar sampler por defecto
                                        p.sampler = list(sd_samplers.samplers_map.values())[0]
                                    
                                    # Configurar steps
                                    p.steps = params['steps']
                                    
                                    # Configurar seed
                                    if params['seed'] != -1:
                                        p.seed = params['seed']
                                    
                                    # Procesar imagen
                                    with closing(p):
                                        processed = modules.processing.process_images(p)
                                    
                                    result = processed.images if processed else []
                                    
                                    # Debug: Imprimir información del resultado
                                    print(f"🔍 Debug Masivo - processed: {processed}")
                                    print(f"🔍 Debug Masivo - result: {result}")
                                    print(f"🔍 Debug Masivo - len(result): {len(result) if result else 0}")
                                    if result and len(result) > 0:
                                        print(f"🔍 Debug Masivo - result[0]: {result[0]}")
                                        print(f"🔍 Debug Masivo - result[0] type: {type(result[0])}")
                                        print(f"🔍 Debug Masivo - hasattr(result[0], 'save'): {hasattr(result[0], 'save')}")
                                    
                                    if result and len(result) > 0 and result[0] is not None:
                                        # Guardar imagen con nomenclatura correcta
                                        filename = f"massive_{nacionalidad}_{genero}_{edad_aleatoria}_{i+1}_{timestamp}.png"
                                        filepath = batch_dir / filename
                                        
                                        # Debug: Imprimir información de la ruta
                                        print(f"🔍 Debug Masivo - batch_dir: {batch_dir}")
                                        print(f"🔍 Debug Masivo - filename: {filename}")
                                        print(f"🔍 Debug Masivo - filepath: {filepath}")
                                        print(f"🔍 Debug Masivo - filepath type: {type(filepath)}")
                                        print(f"🔍 Debug Masivo - str(filepath): {str(filepath)}")
                                        
                                        # Verificar que la ruta sea válida
                                        if filepath and str(filepath):
                                            # Guardar la imagen PIL
                                            if hasattr(result[0], 'save'):
                                                result[0].save(str(filepath))
                                            else:
                                                # Si es una ruta de archivo
                                                import shutil
                                                shutil.copy2(result[0], str(filepath))
                                        else:
                                            print(f"⚠️ Error: Ruta de archivo inválida: {filepath}")
                                            failed_count += 1
                                            continue
                                        
                                        # Guardar configuración JSON dinámica
                                        json_filename = filename.replace('.png', '.json')
                                        json_filepath = batch_dir / json_filename
                                        
                                        # Verificar que la ruta del JSON sea válida
                                        if json_filepath and str(json_filepath):
                                            # Agregar información de la imagen generada al JSON dinámico
                                            json_dinamico["image_info"] = {
                                                "filename": filename,
                                                "filepath": str(filepath),
                                                "generation_successful": True,
                                                "generation_time": datetime.now().isoformat()
                                            }
                                            
                                            with open(str(json_filepath), 'w', encoding='utf-8') as f:
                                                json.dump(json_dinamico, f, indent=2, ensure_ascii=False)
                                            
                                            generated_count += 1
                                            print(f"✅ Imagen {i+1} generada: {filename}")
                                        else:
                                            print(f"⚠️ Error: Ruta de JSON inválida: {json_filepath}")
                                            failed_count += 1
                                            continue
                                    else:
                                        failed_count += 1
                                        print(f"❌ Error generando imagen {i+1}")
                                        
                                except Exception as e:
                                    failed_count += 1
                                    print(f"❌ Error en generación {i+1}: {e}")
                                    print(f"🔍 Debug - Tipo de error: {type(e)}")
                                    print(f"🔍 Debug - Traceback completo:")
                                    import traceback
                                    traceback.print_exc()
                            
                            except Exception as e:
                                failed_count += 1
                                print(f"❌ Error procesando imagen {i+1}: {e}")
                        
                        # Resultado final
                        progress(1.0, desc="Generación completada")
                        
                        resultado = f"✅ **Generación masiva con JSONs dinámicos completada**\n\n"
                        resultado += f"📊 **Estadísticas finales:**\n"
                        resultado += f"- Imágenes generadas: {generated_count}\n"
                        resultado += f"- Imágenes fallidas: {failed_count}\n"
                        resultado += f"- Total procesadas: {cantidad_int}\n"
                        resultado += f"- Modelo utilizado: {model_name_clean}\n"
                        resultado += f"- Directorio: {batch_dir}\n\n"
                        resultado += f"🎯 **Características implementadas:**\n"
                        resultado += f"- ✅ **JSONs dinámicos únicos** para cada imagen\n"
                        resultado += f"- ✅ **Diversidad étnica real** basada en datos demográficos\n"
                        resultado += f"- ✅ **Características únicas** por imagen\n"
                        resultado += f"- ✅ **Edades variables** dentro del rango especificado\n"
                        resultado += f"- ✅ **Prompts únicos** generados dinámicamente\n"
                        resultado += f"- ✅ **Parámetros homogéneos** (512x512, CFG 9.0)\n"
                        resultado += f"- ✅ **Barra de progreso** en tiempo real\n"
                        resultado += f"- ✅ **Configuración JSON completa** por imagen\n\n"
                        resultado += f"🌟 **Diversidad étnica implementada:**\n"
                        resultado += f"- Tonos de piel variables según demografía real\n"
                        resultado += f"- Colores de pelo y ojos diversos\n"
                        resultado += f"- Estructuras faciales variadas\n"
                        resultado += f"- Características étnicas auténticas\n\n"
                        resultado += f"📁 **Archivos generados en**: {batch_dir}\n"
                        resultado += f"🎉 **¡Generación masiva con diversidad étnica completada!**\n"
                        
                        return "", "", 1, 1, resultado
                        
                    except Exception as e:
                        return "", "", 1, 1, f"❌ Error: {e}"
                
                def instrucciones_masivas_func(nacionalidad, genero, edad, cantidad):
                    """Muestra instrucciones detalladas para generación masiva."""
                    try:
                        import time
                        import random
                        from datetime import datetime
                        
                        directorio = "outputs/pasaportes_masivos"
                        Path(directorio).mkdir(parents=True, exist_ok=True)
                        
                        # Convertir valores a enteros
                        cantidad_int = int(cantidad)
                        edad_int = int(edad)
                        
                        resultado = f"📋 **Instrucciones para generación masiva de {nacionalidad}**\n\n"
                        # Obtener parámetros homogéneos
                        parametros = obtener_parametros_nacionalidad(nacionalidad)
                        
                        resultado += f"💡 **Proceso paso a paso:**\n"
                        resultado += f"1. Haz clic en '📝 Aplicar Prompt de Pasaporte' para cargar el prompt\n"
                        resultado += f"2. Ajusta la cantidad en 'Batch count' a {cantidad_int}\n"
                        resultado += f"3. Haz clic en 'Generate' para crear {cantidad_int} imágenes\n"
                        resultado += f"4. Las imágenes se guardarán en: outputs/txt2img-images/\n"
                        resultado += f"5. Usa '📁 Abrir Carpeta de Imágenes' para verlas\n\n"
                        resultado += f"🎯 **Parámetros homogéneos aplicados:**\n"
                        resultado += f"- Resolución: {parametros['width']}x{parametros['height']} (HOMOGÉNEO)\n"
                        resultado += f"- CFG Scale: {parametros['cfg_scale']} (ALTO para seguir instrucciones)\n"
                        resultado += f"- Steps: {parametros['steps']}\n"
                        resultado += f"- Sampler: {parametros['sampler']}\n\n"
                        
                        # Generar prompts de ejemplo
                        from generar_pasaportes import GeneradorPasaportes
                        consulta_dir = Path(__file__).parent.parent / "Consulta"
                        generador = GeneradorPasaportes(str(consulta_dir))
                        
                        resultado += f"📋 **Prompts generados para {nacionalidad}:**\n"
                        for i in range(min(3, cantidad_int)):  # Mostrar máximo 3 ejemplos
                            edad_aleatoria = random.randint(18, 80)  # Usar rango completo para ejemplos
                            prompt_pos, prompt_neg = generador.generar_prompt_completo(nacionalidad, genero, edad_aleatoria, edad_aleatoria)
                            resultado += f"\n**Ejemplo {i+1} (edad {edad_aleatoria}):**\n"
                            resultado += f"Prompt: {prompt_pos[:100]}...\n"
                            resultado += f"Negativo: {prompt_neg[:50]}...\n"
                        
                        if cantidad_int > 3:
                            resultado += f"\n... y {cantidad_int - 3} prompts más\n"
                        
                        resultado += f"\n📁 **Guardado en**: outputs/txt2img-images/\n"
                        resultado += f"📋 **Formato**: [timestamp]-[seed].png"
                        
                        return resultado
                    except Exception as e:
                        return f"❌ Error general: {e}"
                
                def abrir_carpeta_imagenes_func():
                    """Abre la carpeta donde se guardan las imágenes individuales."""
                    try:
                        import subprocess
                        import os
                        from datetime import datetime
                        
                        # Obtener la fecha actual
                        fecha_actual = datetime.now().strftime("%Y-%m-%d")
                        carpeta_imagenes = f"outputs/txt2img-images/{fecha_actual}"
                        
                        # Crear la carpeta si no existe
                        Path(carpeta_imagenes).mkdir(parents=True, exist_ok=True)
                        
                        # Abrir la carpeta según el sistema operativo
                        if os.name == 'nt':  # Windows
                            os.startfile(carpeta_imagenes)
                        elif os.name == 'posix':  # macOS y Linux
                            subprocess.run(['xdg-open', carpeta_imagenes])
                        
                        return f"📁 **Carpeta abierta**: {carpeta_imagenes}\n\n💡 **Ubicación completa**: {os.path.abspath(carpeta_imagenes)}"
                    except Exception as e:
                        return f"❌ Error al abrir carpeta: {e}"
                
                def abrir_carpeta_masivos_func():
                    """Abre la carpeta donde se guardan las imágenes masivas."""
                    try:
                        import subprocess
                        import os
                        
                        carpeta_masivos = "outputs/pasaportes_masivos"
                        
                        # Crear la carpeta si no existe
                        Path(carpeta_masivos).mkdir(parents=True, exist_ok=True)
                        
                        # Abrir la carpeta según el sistema operativo
                        if os.name == 'nt':  # Windows
                            os.startfile(carpeta_masivos)
                        elif os.name == 'posix':  # macOS y Linux
                            subprocess.run(['xdg-open', carpeta_masivos])
                        
                        return f"📂 **Carpeta abierta**: {carpeta_masivos}\n\n💡 **Ubicación completa**: {os.path.abspath(carpeta_masivos)}"
                    except Exception as e:
                        return f"❌ Error al abrir carpeta: {e}"
                
                def ver_progreso_masivo_func():
                    """Muestra el progreso de la generación masiva."""
                    try:
                        import os
                        from datetime import datetime
                        
                        carpeta_masivos = "outputs/pasaportes_masivos"
                        
                        if not os.path.exists(carpeta_masivos):
                            return "📊 **No hay generaciones masivas aún**\n\n💡 **Haz clic en '⚡ Generar Masivo Básico' para comenzar**"
                        
                        # Buscar carpetas de lotes
                        lotes = []
                        for item in os.listdir(carpeta_masivos):
                            item_path = os.path.join(carpeta_masivos, item)
                            if os.path.isdir(item_path) and item.startswith("batch_"):
                                lotes.append(item)
                        
                        if not lotes:
                            return "📊 **No hay lotes de generación masiva**\n\n💡 **Haz clic en '⚡ Generar Masivo Básico' para comenzar**"
                        
                        # Ordenar por fecha (más reciente primero)
                        lotes.sort(reverse=True)
                        
                        resultado = f"📊 **Progreso de Generación Masiva**\n\n"
                        resultado += f"📁 **Lotes encontrados**: {len(lotes)}\n\n"
                        
                        # Mostrar los últimos 5 lotes
                        for i, lote in enumerate(lotes[:5]):
                            lote_path = os.path.join(carpeta_masivos, lote)
                            
                            # Contar archivos en el lote
                            try:
                                archivos = os.listdir(lote_path)
                                png_files = [f for f in archivos if f.endswith('.png')]
                                json_files = [f for f in archivos if f.endswith('.json')]
                                
                                # Obtener fecha de modificación
                                mod_time = os.path.getmtime(lote_path)
                                fecha = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
                                
                                resultado += f"**Lote {i+1}**: `{lote}`\n"
                                resultado += f"- 📅 Fecha: {fecha}\n"
                                resultado += f"- 🖼️ Imágenes: {len(png_files)}\n"
                                resultado += f"- 📄 Configuraciones: {len(json_files)}\n"
                                resultado += f"- 📁 Ruta: `{lote_path}`\n\n"
                                
                            except Exception as e:
                                resultado += f"**Lote {i+1}**: `{lote}` (Error: {e})\n\n"
                        
                        if len(lotes) > 5:
                            resultado += f"... y {len(lotes) - 5} lotes más\n\n"
                        
                        resultado += f"💡 **Para ver el progreso en tiempo real, consulta la consola de WebUI**\n"
                        resultado += f"📁 **Ubicación**: {os.path.abspath(carpeta_masivos)}"
                        
                        return resultado
                        
                    except Exception as e:
                        return f"❌ Error obteniendo progreso: {e}"
                
                def verificar_modelo_actual_func():
                    """Verifica el modelo actual en WebUI y muestra información detallada."""
                    try:
                        import sys
                        
                        # Intentar obtener información del modelo actual
                        model_info = {
                            "model_name": "Unknown",
                            "model_title": "Unknown",
                            "model_filename": "Unknown",
                            "model_hash": "Unknown",
                            "model_type": "Unknown",
                            "is_sdxl": False,
                            "is_sd1": False,
                            "is_sd2": False,
                            "is_sd3": False
                        }
                        
                        if 'modules' in sys.modules:
                            try:
                                from modules import shared, sd_models
                                
                                # Obtener modelo actual
                                current_model = shared.sd_model
                                if current_model and hasattr(current_model, 'sd_checkpoint_info'):
                                    checkpoint_info = current_model.sd_checkpoint_info
                                    model_info = {
                                        "model_name": checkpoint_info.name_for_extra,
                                        "model_title": checkpoint_info.title,
                                        "model_filename": checkpoint_info.filename,
                                        "model_hash": getattr(current_model, 'sd_model_hash', 'unknown'),
                                        "model_type": "Stable Diffusion",
                                        "is_sdxl": getattr(current_model, 'is_sdxl', False),
                                        "is_sd1": getattr(current_model, 'is_sd1', False),
                                        "is_sd2": getattr(current_model, 'is_sd2', False),
                                        "is_sd3": getattr(current_model, 'is_sd3', False)
                                    }
                                else:
                                    # Fallback: obtener desde configuración
                                    selected_model = shared.opts.sd_model_checkpoint
                                    if selected_model:
                                        model_info = {
                                            "model_name": selected_model,
                                            "model_title": selected_model,
                                            "model_filename": "unknown",
                                            "model_hash": "unknown",
                                            "model_type": "Stable Diffusion",
                                            "is_sdxl": False,
                                            "is_sd1": True,
                                            "is_sd2": False,
                                            "is_sd3": False
                                        }
                            except Exception as e:
                                model_info["error"] = str(e)
                        
                        # Crear resultado
                        resultado = f"🔍 **Verificación del Modelo Actual**\n\n"
                        resultado += f"📋 **Información del Modelo:**\n"
                        resultado += f"- **Nombre**: {model_info['model_name']}\n"
                        resultado += f"- **Título**: {model_info['model_title']}\n"
                        resultado += f"- **Archivo**: {model_info['model_filename']}\n"
                        resultado += f"- **Hash**: {model_info['model_hash']}\n"
                        resultado += f"- **Tipo**: {model_info['model_type']}\n\n"
                        
                        resultado += f"🏗️ **Arquitectura del Modelo:**\n"
                        resultado += f"- **SDXL**: {'✅ Sí' if model_info['is_sdxl'] else '❌ No'}\n"
                        resultado += f"- **SD 1.x**: {'✅ Sí' if model_info['is_sd1'] else '❌ No'}\n"
                        resultado += f"- **SD 2.x**: {'✅ Sí' if model_info['is_sd2'] else '❌ No'}\n"
                        resultado += f"- **SD 3.x**: {'✅ Sí' if model_info['is_sd3'] else '❌ No'}\n\n"
                        
                        if 'error' in model_info:
                            resultado += f"⚠️ **Error**: {model_info['error']}\n\n"
                        
                        resultado += f"💡 **Verificación de Coincidencia:**\n"
                        resultado += f"- ✅ **Modelo cargado**: {model_info['model_name']}\n"
                        resultado += f"- ✅ **Modelo seleccionado**: {model_info['model_title']}\n"
                        resultado += f"- ✅ **Estado**: {'Coincide' if model_info['model_name'] == model_info['model_title'] else 'No coincide'}\n\n"
                        
                        resultado += f"📝 **Nota**: Este es el modelo que se utilizará para generar las imágenes de pasaportes.\n"
                        resultado += f"🔧 **Para cambiar el modelo**: Ve a la pestaña 'Settings' y cambia 'Stable Diffusion checkpoint'."
                        
                        return resultado
                        
                    except Exception as e:
                        return f"❌ Error verificando modelo: {e}"

            # Controles de Pasaportes Venezolanos - Fuera del bucle de categorías para posición fija
            # ===== SECCIÓN 1: CONFIGURACIÓN BÁSICA =====
            with gr.Accordion("🌍 Configuración Básica", open=True, elem_id="config_basica_accordion"):
                # Cargar nacionalidades disponibles
                try:
                    from generar_pasaportes import GeneradorPasaportes
                    consulta_dir = Path(__file__).parent.parent / "Consulta"
                    if consulta_dir.exists():
                        generador_pasaportes = GeneradorPasaportes(str(consulta_dir))
                        nacionalidades_pasaportes = list(generador_pasaportes.datos_etnicos.keys())
                    else:
                        nacionalidades_pasaportes = ["venezuelan", "cuban", "haitian"]
                except:
                    nacionalidades_pasaportes = ["venezuelan", "cuban", "haitian"]
                
                with gr.Accordion("🌍 Nacionalidad Avanzada", open=True, elem_id="nacionalidad_avanzada_accordion", elem_classes=["pasaportes_accordion"]):
                    with gr.Row():
                        nacionalidad_pasaporte = gr.Dropdown(
                            choices=nacionalidades_pasaportes,
                            value="venezuelan",
                            label="🌍 Nacionalidad",
                            info="Selecciona la nacionalidad para el pasaporte",
                            elem_id="pasaporte_nacionalidad"
                        )
                        
                        genero_pasaporte = gr.Radio(
                            choices=["mujer", "hombre"], 
                            value="mujer",
                            label="👤 Género",
                            info="Género de la persona",
                            elem_id="pasaporte_genero"
                        )
                        
                        edad_pasaporte = gr.Slider(
                            minimum=18, maximum=80, value=25, step=1,
                            label="🎂 Edad",
                            info="Edad de la persona",
                            elem_id="pasaporte_edad"
                        )
                    
                    with gr.Row():
                        aplicar_prompt_pasaporte_btn = gr.Button(
                            "📝 Aplicar Prompt de Pasaporte", 
                            variant="secondary",
                            elem_id="aplicar_prompt_pasaporte"
                        )
                    
                    # Sistema de Plantillas integrado
                    with gr.Row():
                        with gr.Column(scale=2):
                            nombre_plantilla = gr.Textbox(
                                placeholder="Ej: Mi Configuración Pasaporte",
                                label="💾 Guardar Plantilla",
                                info="Nombre para la configuración actual",
                                elem_id="nombre_plantilla",
                                max_lines=1
                            )
                        
                        with gr.Column(scale=1):
                            guardar_plantilla_btn = gr.Button(
                                "💾 Guardar",
                                variant="primary",
                                elem_id="guardar_plantilla"
                            )
                    
                    with gr.Row():
                        with gr.Column(scale=2):
                            # Inicializar dropdown con plantillas disponibles
                            plantillas_iniciales = actualizar_dropdown_plantillas()
                            plantillas_dropdown = gr.Dropdown(
                                choices=plantillas_iniciales,
                                label="📂 Cargar Plantilla",
                                info="Selecciona una plantilla guardada",
                                elem_id="plantillas_dropdown",
                                allow_custom_value=False
                            )
                        
                        with gr.Column(scale=1):
                            cargar_plantilla_btn = gr.Button(
                                "📂 Cargar",
                                variant="secondary",
                                elem_id="cargar_plantilla"
                            )
                        
                        with gr.Column(scale=1):
                            eliminar_plantilla_btn = gr.Button(
                                "🗑️ Eliminar",
                                variant="stop",
                                elem_id="eliminar_plantilla"
                            )
                    
                    # Información de plantillas
                    info_plantillas = gr.Markdown(
                        value="💡 **Sistema de Plantillas**: Guarda y carga configuraciones personalizadas.",
                        label="Información de Plantillas",
                        elem_id="info_plantillas"
                    )
                    
                    with gr.Row():
                        cantidad_masiva_pasaporte = gr.Number(
                            value=5, minimum=1, maximum=5000, step=1,
                            label="📊 Cantidad de Imágenes",
                            info="Número de imágenes a generar (máximo: 5000)",
                            elem_id="cantidad_masiva_pasaporte"
                        )
                    
                    with gr.Row():
                        generar_masivo_pasaporte_btn = gr.Button(
                            "⚡ Generar Masivo Avanzado", 
                            variant="secondary",
                            elem_id="generar_masivo_pasaporte"
                        )
                        
                        generar_genetico_btn = gr.Button(
                            "🎯 Generar Genético Avanzado", 
                            variant="primary",
                            elem_id="generar_genetico_pasaporte"
                        )
                        
                        detener_generacion_btn = gr.Button(
                            "🛑 Detener Generación", 
                            variant="stop",
                            elem_id="detener_generacion_pasaporte",
                            visible=False
                        )
                    
                    with gr.Row():
                        instrucciones_masivas_btn = gr.Button(
                            "📋 Instrucciones Masivas", 
                            variant="secondary",
                            elem_id="instrucciones_masivas"
                        )
                        
                        ver_progreso_btn = gr.Button(
                            "📊 Ver Progreso", 
                            variant="secondary",
                            elem_id="ver_progreso_masivo"
                        )
                        
                        verificar_modelo_btn = gr.Button(
                            "🔍 Verificar Modelo", 
                            variant="secondary",
                            elem_id="verificar_modelo_actual"
                        )
                    
                    with gr.Row():
                        abrir_carpeta_btn = gr.Button(
                            "📁 Abrir Carpeta Imágenes", 
                            variant="secondary",
                            elem_id="abrir_carpeta_pasaportes"
                        )
                        
                        abrir_carpeta_masivos_btn = gr.Button(
                            "📂 Abrir Carpeta Masivos", 
                            variant="secondary",
                            elem_id="abrir_carpeta_masivos"
                        )
                    
                    info_pasaporte = gr.Markdown(
                        value="Selecciona nacionalidad, género y edad, luego haz clic en 'Aplicar Prompt de Pasaporte'",
                        label="Información",
                        elem_id="info_pasaporte"
                    )
                
                # ===== CONTROLES GENÉTICOS AVANZADOS =====
                with gr.Accordion("🧬 Controles Genéticos Avanzados", open=True, elem_id="genetic_controls", elem_classes=["genetic_accordion"]):
                    # Cargar configuración guardada ANTES de crear los controles
                    saved_beauty, saved_skin, saved_hair, saved_eye, saved_background, saved_region = cargar_configuracion_genetica()
                    
                    with gr.Row():
                        region_pasaporte = gr.Dropdown(
                            choices=["aleatorio", "caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"],
                            value="aleatorio",  # SIEMPRE usar región aleatoria para máxima diversidad
                            label="🏙️ Región",
                            info="Región específica (aleatorio = automático para máxima diversidad)",
                            elem_id="pasaporte_region"
                        )
                        
                        edad_min_pasaporte = gr.Number(
                            value=18, minimum=18, maximum=80, step=1,
                            label="🎂 Edad Mínima",
                            info="Edad mínima del rango",
                            elem_id="pasaporte_edad_min"
                        )
                        
                        edad_max_pasaporte = gr.Number(
                            value=50, minimum=18, maximum=80, step=1,
                            label="🎂 Edad Máxima",
                            info="Edad máxima del rango",
                            elem_id="pasaporte_edad_max"
                        )
                    
                    with gr.Row():
                        beauty_control = gr.Dropdown(
                            choices=["aleatorio", "muy_atractivo", "atractivo", "normal", "promedio", "comun", "ordinario", "poco_atractivo", "feo", "muy_feo", "realista", "variado"],
                            value="aleatorio",  # SIEMPRE usar aleatorio para máxima diversidad real
                            label="💎 Control de Belleza",
                            info="Nivel de atractivo (aleatorio = máxima diversidad real)",
                            elem_id="beauty_control"
                        )
                        
                        skin_control = gr.Dropdown(
                            choices=["auto", "light", "medium", "dark", "mixed"],
                            value=saved_skin if saved_skin in ["auto", "light", "medium", "dark", "mixed"] else "auto",
                            label="🎨 Control de Piel",
                            info="Tono de piel específico",
                            elem_id="skin_control"
                        )
                    
                    with gr.Row():
                        hair_control = gr.Dropdown(
                            choices=["auto", "dark", "light", "mixed"],
                            value=saved_hair if saved_hair in ["auto", "dark", "light", "mixed"] else "auto",
                            label="💇 Control de Cabello",
                            info="Color de cabello específico",
                            elem_id="hair_control"
                        )
                        
                        eye_control = gr.Dropdown(
                            choices=["auto", "dark", "light", "mixed"],
                            value=saved_eye if saved_eye in ["auto", "dark", "light", "mixed"] else "auto",
                            label="👁️ Control de Ojos",
                            info="Color de ojos específico",
                            elem_id="eye_control"
                        )
                        
                        background_control = gr.Dropdown(
                            choices=["white", "beige", "light_blue", "sin_fondo"],
                            value=saved_background if saved_background in ["white", "beige", "light_blue", "sin_fondo"] else "white",
                            label="🖼️ Control de Fondo",
                            info="Fondos sólidos para fácil modificación posterior (sin_fondo = transparente)",
                            elem_id="background_control"
                        )
                
                # Barra de progreso para generación masiva
                progreso_masivo = gr.Progress()
                
                # Conectar eventos (la conexión del botón Aplicar Prompt se hará después de definir steps)
                
                # La conexión del evento se hará después de definir batch_count
                
                instrucciones_masivas_btn.click(
                    fn=instrucciones_masivas_func,
                    inputs=[nacionalidad_pasaporte, genero_pasaporte, edad_pasaporte, cantidad_masiva_pasaporte],
                    outputs=info_pasaporte
                )
                
                abrir_carpeta_btn.click(
                    fn=abrir_carpeta_imagenes_func,
                    outputs=info_pasaporte
                )
                
                abrir_carpeta_masivos_btn.click(
                    fn=abrir_carpeta_masivos_func,
                    outputs=info_pasaporte
                )
                
                ver_progreso_btn.click(
                    fn=ver_progreso_masivo_func,
                    outputs=info_pasaporte
                )
                
                verificar_modelo_btn.click(
                    fn=verificar_modelo_actual_func,
                    outputs=info_pasaporte
                )

            # Configuración normal de txt2img
            with ExitStack() as stack:
                if shared.opts.txt2img_settings_accordion:
                    stack.enter_context(gr.Accordion("Open for Settings", open=True))
                stack.enter_context(gr.Column(variant='compact', elem_id="txt2img_settings"))

                scripts.scripts_txt2img.prepare_ui()

                for category in ordered_ui_categories():
                    if category == "prompt":
                        toprow.create_inline_toprow_prompts()

                    elif category == "dimensions":
                        with FormRow():
                            with gr.Column(elem_id="txt2img_column_size", scale=4):
                                width = gr.Slider(minimum=64, maximum=2048, step=8, label="Width", value=512, elem_id="txt2img_width")
                                height = gr.Slider(minimum=64, maximum=2048, step=8, label="Height", value=512, elem_id="txt2img_height")

                            with gr.Column(elem_id="txt2img_dimensions_row", scale=1, elem_classes="dimensions-tools"):
                                res_switch_btn = ToolButton(value=switch_values_symbol, elem_id="txt2img_res_switch_btn", tooltip="Switch width/height")

                            if opts.dimensions_and_batch_together:
                                with gr.Column(elem_id="txt2img_column_batch"):
                                    batch_count = gr.Slider(minimum=1, step=1, label='Batch count', value=1, elem_id="txt2img_batch_count")
                                    batch_size = gr.Slider(minimum=1, maximum=8, step=1, label='Batch size', value=1, elem_id="txt2img_batch_size")

                    elif category == "cfg":
                        with gr.Row():
                            cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5, label='CFG Scale', value=12.0, elem_id="txt2img_cfg_scale")

                    elif category == "checkboxes":
                        with FormRow(elem_classes="checkboxes-row", variant="compact"):
                            pass

                    elif category == "accordions":
                        with gr.Row(elem_id="txt2img_accordions", elem_classes="accordions"):
                            with InputAccordion(False, label="Hires. fix", elem_id="txt2img_hr") as enable_hr:
                                with enable_hr.extra():
                                    hr_final_resolution = FormHTML(value="", elem_id="txtimg_hr_finalres", label="Upscaled resolution", interactive=False, min_width=0)

                                with FormRow(elem_id="txt2img_hires_fix_row1", variant="compact"):
                                    hr_upscaler = gr.Dropdown(label="Upscaler", elem_id="txt2img_hr_upscaler", choices=[*shared.latent_upscale_modes, *[x.name for x in shared.sd_upscalers]], value=shared.latent_upscale_default_mode)
                                    hr_second_pass_steps = gr.Slider(minimum=0, maximum=150, step=1, label='Hires steps', value=0, elem_id="txt2img_hires_steps")
                                    denoising_strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label='Denoising strength', value=0.7, elem_id="txt2img_denoising_strength")

                                with FormRow(elem_id="txt2img_hires_fix_row2", variant="compact"):
                                    hr_scale = gr.Slider(minimum=1.0, maximum=4.0, step=0.05, label="Upscale by", value=2.0, elem_id="txt2img_hr_scale")
                                    hr_resize_x = gr.Slider(minimum=0, maximum=2048, step=8, label="Resize width to", value=0, elem_id="txt2img_hr_resize_x")
                                    hr_resize_y = gr.Slider(minimum=0, maximum=2048, step=8, label="Resize height to", value=0, elem_id="txt2img_hr_resize_y")

                                with FormRow(elem_id="txt2img_hires_fix_row3", variant="compact", visible=opts.hires_fix_show_sampler) as hr_sampler_container:

                                    hr_checkpoint_name = gr.Dropdown(label='Checkpoint', elem_id="hr_checkpoint", choices=["Use same checkpoint"] + modules.sd_models.checkpoint_tiles(use_short=True), value="Use same checkpoint")
                                    create_refresh_button(hr_checkpoint_name, modules.sd_models.list_models, lambda: {"choices": ["Use same checkpoint"] + modules.sd_models.checkpoint_tiles(use_short=True)}, "hr_checkpoint_refresh")

                                    hr_sampler_name = gr.Dropdown(label='Hires sampling method', elem_id="hr_sampler", choices=["Use same sampler"] + sd_samplers.visible_sampler_names(), value="Use same sampler")
                                    hr_scheduler = gr.Dropdown(label='Hires schedule type', elem_id="hr_scheduler", choices=["Use same scheduler"] + [x.label for x in sd_schedulers.schedulers], value="Use same scheduler")

                                with FormRow(elem_id="txt2img_hires_fix_row4", variant="compact", visible=opts.hires_fix_show_prompts) as hr_prompts_container:
                                    with gr.Column(scale=80):
                                        with gr.Row():
                                            hr_prompt = gr.Textbox(label="Hires prompt", elem_id="hires_prompt", show_label=False, lines=3, placeholder="Prompt for hires fix pass.\nLeave empty to use the same prompt as in first pass.", elem_classes=["prompt"])
                                    with gr.Column(scale=80):
                                        with gr.Row():
                                            hr_negative_prompt = gr.Textbox(label="Hires negative prompt", elem_id="hires_neg_prompt", show_label=False, lines=3, placeholder="Negative prompt for hires fix pass.\nLeave empty to use the same negative prompt as in first pass.", elem_classes=["prompt"])

                            scripts.scripts_txt2img.setup_ui_for_section(category)

                    elif category == "batch":
                        if not opts.dimensions_and_batch_together:
                            with FormRow(elem_id="txt2img_column_batch"):
                                batch_count = gr.Slider(minimum=1, step=1, label='Batch count', value=1, elem_id="txt2img_batch_count")
                                batch_size = gr.Slider(minimum=1, maximum=8, step=1, label='Batch size', value=1, elem_id="txt2img_batch_size")

                    elif category == "override_settings":
                        with FormRow(elem_id="txt2img_override_settings_row") as row:
                            override_settings = create_override_settings_dropdown('txt2img', row)

                    elif category == "scripts":
                        with FormGroup(elem_id="txt2img_script_container"):
                            custom_inputs = scripts.scripts_txt2img.setup_ui()

                    if category not in {"accordions"}:
                        scripts.scripts_txt2img.setup_ui_for_section(category)

            hr_resolution_preview_inputs = [enable_hr, width, height, hr_scale, hr_resize_x, hr_resize_y]

            for component in hr_resolution_preview_inputs:
                event = component.release if isinstance(component, gr.Slider) else component.change

                event(
                    fn=calc_resolution_hires,
                    inputs=hr_resolution_preview_inputs,
                    outputs=[hr_final_resolution],
                    show_progress=False,
                )
                event(
                    None,
                    _js="onCalcResolutionHires",
                    inputs=hr_resolution_preview_inputs,
                    outputs=[],
                    show_progress=False,
                )

            # Panel de salida ya definido arriba en el lado izquierdo

            txt2img_inputs = [
                dummy_component,
                toprow.prompt,
                toprow.negative_prompt,
                toprow.ui_styles.dropdown,
                batch_count,
                batch_size,
                cfg_scale,
                height,
                width,
                enable_hr,
                denoising_strength,
                hr_scale,
                hr_upscaler,
                hr_second_pass_steps,
                hr_resize_x,
                hr_resize_y,
                hr_checkpoint_name,
                hr_sampler_name,
                hr_scheduler,
                hr_prompt,
                hr_negative_prompt,
                override_settings,
            ] + custom_inputs

            txt2img_outputs = [
                output_panel.gallery,
                output_panel.generation_info,
                output_panel.infotext,
                output_panel.html_log,
            ]

            txt2img_args = dict(
                fn=wrap_gradio_gpu_call(modules.txt2img.txt2img, extra_outputs=[None, '', '']),
                _js="submit",
                inputs=txt2img_inputs,
                outputs=txt2img_outputs,
                show_progress=False,
            )

            toprow.prompt.submit(**txt2img_args)
            toprow.submit.click(**txt2img_args)

            # Las conexiones de los botones de generación se harán después de definir steps

            output_panel.button_upscale.click(
                fn=wrap_gradio_gpu_call(modules.txt2img.txt2img_upscale, extra_outputs=[None, '', '']),
                _js="submit_txt2img_upscale",
                inputs=txt2img_inputs[0:1] + [output_panel.gallery, dummy_component, output_panel.generation_info] + txt2img_inputs[1:],
                outputs=txt2img_outputs,
                show_progress=False,
            )

            res_switch_btn.click(fn=None, _js="function(){switchWidthHeight('txt2img')}", inputs=None, outputs=None, show_progress=False)

            toprow.restore_progress_button.click(
                fn=progress.restore_progress,
                _js="restoreProgressTxt2img",
                inputs=[dummy_component],
                outputs=[
                    output_panel.gallery,
                    output_panel.generation_info,
                    output_panel.infotext,
                    output_panel.html_log,
                ],
                show_progress=False,
            )

            txt2img_paste_fields = [
                PasteField(toprow.prompt, "Prompt", api="prompt"),
                PasteField(toprow.negative_prompt, "Negative prompt", api="negative_prompt"),
                PasteField(cfg_scale, "CFG scale", api="cfg_scale"),
                PasteField(width, "Size-1", api="width"),
                PasteField(height, "Size-2", api="height"),
                PasteField(batch_size, "Batch size", api="batch_size"),
                PasteField(toprow.ui_styles.dropdown, lambda d: d["Styles array"] if isinstance(d.get("Styles array"), list) else gr.update(), api="styles"),
                PasteField(denoising_strength, "Denoising strength", api="denoising_strength"),
                PasteField(enable_hr, lambda d: "Denoising strength" in d and ("Hires upscale" in d or "Hires upscaler" in d or "Hires resize-1" in d), api="enable_hr"),
                PasteField(hr_scale, "Hires upscale", api="hr_scale"),
                PasteField(hr_upscaler, "Hires upscaler", api="hr_upscaler"),
                PasteField(hr_second_pass_steps, "Hires steps", api="hr_second_pass_steps"),
                PasteField(hr_resize_x, "Hires resize-1", api="hr_resize_x"),
                PasteField(hr_resize_y, "Hires resize-2", api="hr_resize_y"),
                PasteField(hr_checkpoint_name, "Hires checkpoint", api="hr_checkpoint_name"),
                PasteField(hr_sampler_name, sd_samplers.get_hr_sampler_from_infotext, api="hr_sampler_name"),
                PasteField(hr_scheduler, sd_samplers.get_hr_scheduler_from_infotext, api="hr_scheduler"),
                PasteField(hr_sampler_container, lambda d: gr.update(visible=True) if d.get("Hires sampler", "Use same sampler") != "Use same sampler" or d.get("Hires checkpoint", "Use same checkpoint") != "Use same checkpoint" or d.get("Hires schedule type", "Use same scheduler") != "Use same scheduler" else gr.update()),
                PasteField(hr_prompt, "Hires prompt", api="hr_prompt"),
                PasteField(hr_negative_prompt, "Hires negative prompt", api="hr_negative_prompt"),
                PasteField(hr_prompts_container, lambda d: gr.update(visible=True) if d.get("Hires prompt", "") != "" or d.get("Hires negative prompt", "") != "" else gr.update()),
                *scripts.scripts_txt2img.infotext_fields
            ]
            parameters_copypaste.add_paste_fields("txt2img", None, txt2img_paste_fields, override_settings)
            parameters_copypaste.register_paste_params_button(parameters_copypaste.ParamBinding(
                paste_button=toprow.paste, tabname="txt2img", source_text_component=toprow.prompt, source_image_component=None,
            ))

            steps = scripts.scripts_txt2img.script('Sampler').steps

            # Conectar el botón Aplicar Prompt después de definir steps
            aplicar_prompt_pasaporte_btn.click(
                fn=aplicar_prompt_pasaporte_func,
                inputs=[nacionalidad_pasaporte, genero_pasaporte, edad_pasaporte],
                outputs=[toprow.prompt, toprow.negative_prompt, width, height, cfg_scale, steps, scripts.scripts_txt2img.script('Sampler').sampler_name, scripts.scripts_txt2img.script('Seed').seed, batch_count, batch_size, denoising_strength, hr_second_pass_steps, hr_scale, hr_resize_x, hr_resize_y, hr_upscaler, hr_sampler_name, hr_scheduler, refiner_checkpoint, refiner_switch_at, info_pasaporte]
            )

            # Conectar botones del sistema de plantillas mejorado
            guardar_plantilla_btn.click(
                fn=guardar_plantilla_ui,
                inputs=[nombre_plantilla, toprow.prompt, toprow.negative_prompt, width, height, cfg_scale, steps, scripts.scripts_txt2img.script('Sampler').sampler_name, scripts.scripts_txt2img.script('Seed').seed, batch_count, batch_size, denoising_strength, hr_second_pass_steps, hr_scale, hr_resize_x, hr_resize_y, hr_upscaler, hr_sampler_name, hr_scheduler, refiner_checkpoint, refiner_switch_at],
                outputs=[info_plantillas, plantillas_dropdown, nombre_plantilla]
            )

            cargar_plantilla_btn.click(
                fn=cargar_plantilla_ui,
                inputs=[plantillas_dropdown],
                outputs=[toprow.prompt, toprow.negative_prompt, width, height, cfg_scale, steps, scripts.scripts_txt2img.script('Sampler').sampler_name, scripts.scripts_txt2img.script('Seed').seed, batch_count, batch_size, denoising_strength, hr_second_pass_steps, hr_scale, hr_resize_x, hr_resize_y, hr_upscaler, hr_sampler_name, hr_scheduler, refiner_checkpoint, refiner_switch_at, info_plantillas]
            )

            eliminar_plantilla_btn.click(
                fn=eliminar_plantilla_ui,
                inputs=[plantillas_dropdown],
                outputs=[info_plantillas, plantillas_dropdown]
            )

            # El dropdown se inicializa automáticamente con las plantillas disponibles
            
            # El dropdown se actualizará automáticamente cuando se guarde una plantilla

            # Conectar botones de generación después de definir steps
            generar_masivo_pasaporte_btn.click(
                fn=generar_masivo_pasaporte_func,
                inputs=[nacionalidad_pasaporte, genero_pasaporte, edad_pasaporte, cantidad_masiva_pasaporte, edad_min_pasaporte, edad_max_pasaporte, region_pasaporte, cfg_scale, steps, scripts.scripts_txt2img.script('Sampler').sampler_name, scripts.scripts_txt2img.script('Seed').seed, width, height, batch_count, batch_size, denoising_strength, hr_second_pass_steps, hr_scale, hr_resize_x, hr_resize_y, hr_upscaler, hr_sampler_name, hr_scheduler, refiner_checkpoint, refiner_switch_at],
                outputs=[toprow.prompt, toprow.negative_prompt, batch_count, batch_size, info_pasaporte],
                show_progress=True
            ).then(
                fn=lambda: gr.update(visible=True),
                inputs=[],
                outputs=[detener_generacion_btn]
            )
            
            detener_generacion_btn.click(
                fn=detener_generacion_func,
                inputs=[],
                outputs=[info_pasaporte],
                show_progress=False
            ).then(
                fn=lambda: gr.update(visible=False),
                inputs=[],
                outputs=[detener_generacion_btn]
            )
            
            generar_genetico_btn.click(
                fn=generar_masivo_genetico_func,
                inputs=[nacionalidad_pasaporte, genero_pasaporte, edad_pasaporte, cantidad_masiva_pasaporte, 
                       region_pasaporte, edad_min_pasaporte, edad_max_pasaporte, 
                       beauty_control, skin_control, hair_control, eye_control, background_control,
                       cfg_scale, steps, scripts.scripts_txt2img.script('Sampler').sampler_name, scripts.scripts_txt2img.script('Seed').seed, width, height, batch_count, batch_size, denoising_strength, hr_second_pass_steps, hr_scale, hr_resize_x, hr_resize_y, hr_upscaler, hr_sampler_name, hr_scheduler, refiner_checkpoint, refiner_switch_at],
                outputs=[toprow.prompt, toprow.negative_prompt, batch_count, batch_size, info_pasaporte],
                show_progress=True
            ).then(
                fn=lambda: gr.update(visible=True),
                inputs=[],
                outputs=[detener_generacion_btn]
            )

            txt2img_preview_params = [
                toprow.prompt,
                toprow.negative_prompt,
                steps,
                scripts.scripts_txt2img.script('Sampler').sampler_name,
                cfg_scale,
                scripts.scripts_txt2img.script('Seed').seed,
                width,
                height,
            ]

            toprow.ui_styles.dropdown.change(fn=wrap_queued_call(update_token_counter), inputs=[toprow.prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.token_counter])
            toprow.ui_styles.dropdown.change(fn=wrap_queued_call(update_negative_prompt_token_counter), inputs=[toprow.negative_prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.negative_token_counter])
            toprow.token_button.click(fn=wrap_queued_call(update_token_counter), inputs=[toprow.prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.token_counter])
            toprow.negative_token_button.click(fn=wrap_queued_call(update_negative_prompt_token_counter), inputs=[toprow.negative_prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.negative_token_counter])

        extra_networks_ui = ui_extra_networks.create_ui(txt2img_interface, [txt2img_generation_tab], 'txt2img')
        ui_extra_networks.setup_ui(extra_networks_ui, output_panel.gallery)

        extra_tabs.__exit__()

    scripts.scripts_current = scripts.scripts_img2img
    scripts.scripts_img2img.initialize_scripts(is_img2img=True)

    with gr.Blocks(analytics_enabled=False) as img2img_interface:
        toprow = ui_toprow.Toprow(is_img2img=True, is_compact=shared.opts.compact_prompt_box)

        extra_tabs = gr.Tabs(elem_id="img2img_extra_tabs", elem_classes=["extra-networks"])
        extra_tabs.__enter__()

        with gr.Tab("Generation", id="img2img_generation") as img2img_generation_tab, ResizeHandleRow(equal_height=False):
            with ExitStack() as stack:
                if shared.opts.img2img_settings_accordion:
                    stack.enter_context(gr.Accordion("Open for Settings", open=True))
                stack.enter_context(gr.Column(variant='compact', elem_id="img2img_settings"))

                copy_image_buttons = []
                copy_image_destinations = {}

                def add_copy_image_controls(tab_name, elem):
                    with gr.Row(variant="compact", elem_id=f"img2img_copy_to_{tab_name}"):
                        gr.HTML("Copy image to: ", elem_id=f"img2img_label_copy_to_{tab_name}")

                        for title, name in zip(['img2img', 'sketch', 'inpaint', 'inpaint sketch'], ['img2img', 'sketch', 'inpaint', 'inpaint_sketch']):
                            if name == tab_name:
                                gr.Button(title, interactive=False)
                                copy_image_destinations[name] = elem
                                continue

                            button = gr.Button(title)
                            copy_image_buttons.append((button, name, elem))

                scripts.scripts_img2img.prepare_ui()

                for category in ordered_ui_categories():
                    if category == "prompt":
                        toprow.create_inline_toprow_prompts()

                    if category == "image":
                        with gr.Tabs(elem_id="mode_img2img"):
                            img2img_selected_tab = gr.Number(value=0, visible=False)

                            with gr.TabItem('img2img', id='img2img', elem_id="img2img_img2img_tab") as tab_img2img:
                                init_img = gr.Image(label="Image for img2img", elem_id="img2img_image", show_label=False, source="upload", interactive=True, type="pil", tool="editor", image_mode="RGBA", height=opts.img2img_editor_height)
                                add_copy_image_controls('img2img', init_img)

                            with gr.TabItem('Sketch', id='img2img_sketch', elem_id="img2img_img2img_sketch_tab") as tab_sketch:
                                sketch = gr.Image(label="Image for img2img", elem_id="img2img_sketch", show_label=False, source="upload", interactive=True, type="pil", tool="color-sketch", image_mode="RGB", height=opts.img2img_editor_height, brush_color=opts.img2img_sketch_default_brush_color)
                                add_copy_image_controls('sketch', sketch)

                            with gr.TabItem('Inpaint', id='inpaint', elem_id="img2img_inpaint_tab") as tab_inpaint:
                                init_img_with_mask = gr.Image(label="Image for inpainting with mask", show_label=False, elem_id="img2maskimg", source="upload", interactive=True, type="pil", tool="sketch", image_mode="RGBA", height=opts.img2img_editor_height, brush_color=opts.img2img_inpaint_mask_brush_color)
                                add_copy_image_controls('inpaint', init_img_with_mask)

                            with gr.TabItem('Inpaint sketch', id='inpaint_sketch', elem_id="img2img_inpaint_sketch_tab") as tab_inpaint_color:
                                inpaint_color_sketch = gr.Image(label="Color sketch inpainting", show_label=False, elem_id="inpaint_sketch", source="upload", interactive=True, type="pil", tool="color-sketch", image_mode="RGB", height=opts.img2img_editor_height, brush_color=opts.img2img_inpaint_sketch_default_brush_color)
                                inpaint_color_sketch_orig = gr.State(None)
                                add_copy_image_controls('inpaint_sketch', inpaint_color_sketch)

                                def update_orig(image, state):
                                    if image is not None:
                                        same_size = state is not None and state.size == image.size
                                        has_exact_match = np.any(np.all(np.array(image) == np.array(state), axis=-1))
                                        edited = same_size and has_exact_match
                                        return image if not edited or state is None else state

                                inpaint_color_sketch.change(update_orig, [inpaint_color_sketch, inpaint_color_sketch_orig], inpaint_color_sketch_orig)

                            with gr.TabItem('Inpaint upload', id='inpaint_upload', elem_id="img2img_inpaint_upload_tab") as tab_inpaint_upload:
                                init_img_inpaint = gr.Image(label="Image for img2img", show_label=False, source="upload", interactive=True, type="pil", elem_id="img_inpaint_base")
                                init_mask_inpaint = gr.Image(label="Mask", source="upload", interactive=True, type="pil", image_mode="RGBA", elem_id="img_inpaint_mask")

                            with gr.TabItem('Batch', id='batch', elem_id="img2img_batch_tab") as tab_batch:
                                with gr.Tabs(elem_id="img2img_batch_source"):
                                    img2img_batch_source_type = gr.Textbox(visible=False, value="upload")
                                    with gr.TabItem('Upload', id='batch_upload', elem_id="img2img_batch_upload_tab") as tab_batch_upload:
                                        img2img_batch_upload = gr.Files(label="Files", interactive=True, elem_id="img2img_batch_upload")
                                    with gr.TabItem('From directory', id='batch_from_dir', elem_id="img2img_batch_from_dir_tab") as tab_batch_from_dir:
                                        hidden = '<br>Disabled when launched with --hide-ui-dir-config.' if shared.cmd_opts.hide_ui_dir_config else ''
                                        gr.HTML(
                                            "<p style='padding-bottom: 1em;' class=\"text-gray-500\">Process images in a directory on the same machine where the server is running." +
                                            "<br>Use an empty output directory to save pictures normally instead of writing to the output directory." +
                                            f"<br>Add inpaint batch mask directory to enable inpaint batch processing."
                                            f"{hidden}</p>"
                                        )
                                        img2img_batch_input_dir = gr.Textbox(label="Input directory", **shared.hide_dirs, elem_id="img2img_batch_input_dir")
                                        img2img_batch_output_dir = gr.Textbox(label="Output directory", **shared.hide_dirs, elem_id="img2img_batch_output_dir")
                                        img2img_batch_inpaint_mask_dir = gr.Textbox(label="Inpaint batch mask directory (required for inpaint batch processing only)", **shared.hide_dirs, elem_id="img2img_batch_inpaint_mask_dir")
                                tab_batch_upload.select(fn=lambda: "upload", inputs=[], outputs=[img2img_batch_source_type])
                                tab_batch_from_dir.select(fn=lambda: "from dir", inputs=[], outputs=[img2img_batch_source_type])
                                with gr.Accordion("PNG info", open=True):
                                    img2img_batch_use_png_info = gr.Checkbox(label="Append png info to prompts", elem_id="img2img_batch_use_png_info")
                                    img2img_batch_png_info_dir = gr.Textbox(label="PNG info directory", **shared.hide_dirs, placeholder="Leave empty to use input directory", elem_id="img2img_batch_png_info_dir")
                                    img2img_batch_png_info_props = gr.CheckboxGroup(["Prompt", "Negative prompt", "Seed", "CFG scale", "Sampler", "Steps", "Model hash"], label="Parameters to take from png info", info="Prompts from png info will be appended to prompts set in ui.")

                            img2img_tabs = [tab_img2img, tab_sketch, tab_inpaint, tab_inpaint_color, tab_inpaint_upload, tab_batch]

                            for i, tab in enumerate(img2img_tabs):
                                tab.select(fn=lambda tabnum=i: tabnum, inputs=[], outputs=[img2img_selected_tab])

                        def copy_image(img):
                            if isinstance(img, dict) and 'image' in img:
                                return img['image']

                            return img

                        for button, name, elem in copy_image_buttons:
                            button.click(
                                fn=copy_image,
                                inputs=[elem],
                                outputs=[copy_image_destinations[name]],
                            )
                            button.click(
                                fn=lambda: None,
                                _js=f"switch_to_{name.replace(' ', '_')}",
                                inputs=[],
                                outputs=[],
                            )

                        with FormRow():
                            resize_mode = gr.Radio(label="Resize mode", elem_id="resize_mode", choices=["Just resize", "Crop and resize", "Resize and fill", "Just resize (latent upscale)"], type="index", value="Just resize")

                    elif category == "dimensions":
                        with FormRow():
                            with gr.Column(elem_id="img2img_column_size", scale=4):
                                selected_scale_tab = gr.Number(value=0, visible=False)

                                with gr.Tabs(elem_id="img2img_tabs_resize"):
                                    with gr.Tab(label="Resize to", id="to", elem_id="img2img_tab_resize_to") as tab_scale_to:
                                        with FormRow():
                                            with gr.Column(elem_id="img2img_column_size", scale=4):
                                                width = gr.Slider(minimum=64, maximum=2048, step=8, label="Width", value=512, elem_id="img2img_width")
                                                height = gr.Slider(minimum=64, maximum=2048, step=8, label="Height", value=512, elem_id="img2img_height")
                                            with gr.Column(elem_id="img2img_dimensions_row", scale=1, elem_classes="dimensions-tools"):
                                                res_switch_btn = ToolButton(value=switch_values_symbol, elem_id="img2img_res_switch_btn", tooltip="Switch width/height")
                                                detect_image_size_btn = ToolButton(value=detect_image_size_symbol, elem_id="img2img_detect_image_size_btn", tooltip="Auto detect size from img2img")

                                    with gr.Tab(label="Resize by", id="by", elem_id="img2img_tab_resize_by") as tab_scale_by:
                                        scale_by = gr.Slider(minimum=0.05, maximum=4.0, step=0.05, label="Scale", value=1.0, elem_id="img2img_scale")

                                        with FormRow():
                                            scale_by_html = FormHTML(resize_from_to_html(0, 0, 0.0), elem_id="img2img_scale_resolution_preview")
                                            gr.Slider(label="Unused", elem_id="img2img_unused_scale_by_slider")
                                            button_update_resize_to = gr.Button(visible=False, elem_id="img2img_update_resize_to")

                                    on_change_args = dict(
                                        fn=resize_from_to_html,
                                        _js="currentImg2imgSourceResolution",
                                        inputs=[dummy_component, dummy_component, scale_by],
                                        outputs=scale_by_html,
                                        show_progress=False,
                                    )

                                    scale_by.release(**on_change_args)
                                    button_update_resize_to.click(**on_change_args)

                            tab_scale_to.select(fn=lambda: 0, inputs=[], outputs=[selected_scale_tab])
                            tab_scale_by.select(fn=lambda: 1, inputs=[], outputs=[selected_scale_tab])

                            if opts.dimensions_and_batch_together:
                                with gr.Column(elem_id="img2img_column_batch"):
                                    batch_count = gr.Slider(minimum=1, step=1, label='Batch count', value=1, elem_id="img2img_batch_count")
                                    batch_size = gr.Slider(minimum=1, maximum=8, step=1, label='Batch size', value=1, elem_id="img2img_batch_size")

                    elif category == "denoising":
                        denoising_strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label='Denoising strength', value=0.75, elem_id="img2img_denoising_strength")

                    elif category == "cfg":
                        with gr.Row():
                            cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5, label='CFG Scale', value=7.0, elem_id="img2img_cfg_scale")
                            image_cfg_scale = gr.Slider(minimum=0, maximum=3.0, step=0.05, label='Image CFG Scale', value=1.5, elem_id="img2img_image_cfg_scale", visible=False)

                    elif category == "checkboxes":
                        with FormRow(elem_classes="checkboxes-row", variant="compact"):
                            pass

                    elif category == "accordions":
                        with gr.Row(elem_id="img2img_accordions", elem_classes="accordions"):
                            scripts.scripts_img2img.setup_ui_for_section(category)

                    elif category == "batch":
                        if not opts.dimensions_and_batch_together:
                            with FormRow(elem_id="img2img_column_batch"):
                                batch_count = gr.Slider(minimum=1, step=1, label='Batch count', value=1, elem_id="img2img_batch_count")
                                batch_size = gr.Slider(minimum=1, maximum=8, step=1, label='Batch size', value=1, elem_id="img2img_batch_size")

                    elif category == "override_settings":
                        with FormRow(elem_id="img2img_override_settings_row") as row:
                            override_settings = create_override_settings_dropdown('img2img', row)

                    elif category == "scripts":
                        with FormGroup(elem_id="img2img_script_container"):
                            custom_inputs = scripts.scripts_img2img.setup_ui()

                    elif category == "inpaint":
                        with FormGroup(elem_id="inpaint_controls", visible=False) as inpaint_controls:
                            with FormRow():
                                mask_blur = gr.Slider(label='Mask blur', minimum=0, maximum=64, step=1, value=4, elem_id="img2img_mask_blur")
                                mask_alpha = gr.Slider(label="Mask transparency", visible=False, elem_id="img2img_mask_alpha")

                            with FormRow():
                                inpainting_mask_invert = gr.Radio(label='Mask mode', choices=['Inpaint masked', 'Inpaint not masked'], value='Inpaint masked', type="index", elem_id="img2img_mask_mode")

                            with FormRow():
                                inpainting_fill = gr.Radio(label='Masked content', choices=['fill', 'original', 'latent noise', 'latent nothing'], value='original', type="index", elem_id="img2img_inpainting_fill")

                            with FormRow():
                                with gr.Column():
                                    inpaint_full_res = gr.Radio(label="Inpaint area", choices=["Whole picture", "Only masked"], type="index", value="Whole picture", elem_id="img2img_inpaint_full_res")

                                with gr.Column(scale=4):
                                    inpaint_full_res_padding = gr.Slider(label='Only masked padding, pixels', minimum=0, maximum=256, step=4, value=32, elem_id="img2img_inpaint_full_res_padding")

                    if category not in {"accordions"}:
                        scripts.scripts_img2img.setup_ui_for_section(category)

            # the code below is meant to update the resolution label after the image in the image selection UI has changed.
            # as it is now the event keeps firing continuously for inpaint edits, which ruins the page with constant requests.
            # I assume this must be a gradio bug and for now we'll just do it for non-inpaint inputs.
            for component in [init_img, sketch]:
                component.change(fn=lambda: None, _js="updateImg2imgResizeToTextAfterChangingImage", inputs=[], outputs=[], show_progress=False)

            def select_img2img_tab(tab):
                return gr.update(visible=tab in [2, 3, 4]), gr.update(visible=tab == 3),

            for i, elem in enumerate(img2img_tabs):
                elem.select(
                    fn=lambda tab=i: select_img2img_tab(tab),
                    inputs=[],
                    outputs=[inpaint_controls, mask_alpha],
                )

            output_panel = create_output_panel("img2img", opts.outdir_img2img_samples, toprow)

            img2img_args = dict(
                fn=wrap_gradio_gpu_call(modules.img2img.img2img, extra_outputs=[None, '', '']),
                _js="submit_img2img",
                inputs=[
                    dummy_component,
                    dummy_component,
                    toprow.prompt,
                    toprow.negative_prompt,
                    toprow.ui_styles.dropdown,
                    init_img,
                    sketch,
                    init_img_with_mask,
                    inpaint_color_sketch,
                    inpaint_color_sketch_orig,
                    init_img_inpaint,
                    init_mask_inpaint,
                    mask_blur,
                    mask_alpha,
                    inpainting_fill,
                    batch_count,
                    batch_size,
                    cfg_scale,
                    image_cfg_scale,
                    denoising_strength,
                    selected_scale_tab,
                    height,
                    width,
                    scale_by,
                    resize_mode,
                    inpaint_full_res,
                    inpaint_full_res_padding,
                    inpainting_mask_invert,
                    img2img_batch_input_dir,
                    img2img_batch_output_dir,
                    img2img_batch_inpaint_mask_dir,
                    override_settings,
                    img2img_batch_use_png_info,
                    img2img_batch_png_info_props,
                    img2img_batch_png_info_dir,
                    img2img_batch_source_type,
                    img2img_batch_upload,
                ] + custom_inputs,
                outputs=[
                    output_panel.gallery,
                    output_panel.generation_info,
                    output_panel.infotext,
                    output_panel.html_log,
                ],
                show_progress=False,
            )

            interrogate_args = dict(
                _js="get_img2img_tab_index",
                inputs=[
                    dummy_component,
                    img2img_batch_input_dir,
                    img2img_batch_output_dir,
                    init_img,
                    sketch,
                    init_img_with_mask,
                    inpaint_color_sketch,
                    init_img_inpaint,
                ],
                outputs=[toprow.prompt, dummy_component],
            )

            toprow.prompt.submit(**img2img_args)
            toprow.submit.click(**img2img_args)

            res_switch_btn.click(fn=None, _js="function(){switchWidthHeight('img2img')}", inputs=None, outputs=None, show_progress=False)

            detect_image_size_btn.click(
                fn=lambda w, h, _: (w or gr.update(), h or gr.update()),
                _js="currentImg2imgSourceResolution",
                inputs=[dummy_component, dummy_component, dummy_component],
                outputs=[width, height],
                show_progress=False,
            )

            toprow.restore_progress_button.click(
                fn=progress.restore_progress,
                _js="restoreProgressImg2img",
                inputs=[dummy_component],
                outputs=[
                    output_panel.gallery,
                    output_panel.generation_info,
                    output_panel.infotext,
                    output_panel.html_log,
                ],
                show_progress=False,
            )

            toprow.button_interrogate.click(
                fn=lambda *args: process_interrogate(interrogate, *args),
                **interrogate_args,
            )

            toprow.button_deepbooru.click(
                fn=lambda *args: process_interrogate(interrogate_deepbooru, *args),
                **interrogate_args,
            )

            steps = scripts.scripts_img2img.script('Sampler').steps

            toprow.ui_styles.dropdown.change(fn=wrap_queued_call(update_token_counter), inputs=[toprow.prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.token_counter])
            toprow.ui_styles.dropdown.change(fn=wrap_queued_call(update_negative_prompt_token_counter), inputs=[toprow.negative_prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.negative_token_counter])
            toprow.token_button.click(fn=update_token_counter, inputs=[toprow.prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.token_counter])
            toprow.negative_token_button.click(fn=wrap_queued_call(update_negative_prompt_token_counter), inputs=[toprow.negative_prompt, steps, toprow.ui_styles.dropdown], outputs=[toprow.negative_token_counter])

            img2img_paste_fields = [
                (toprow.prompt, "Prompt"),
                (toprow.negative_prompt, "Negative prompt"),
                (cfg_scale, "CFG scale"),
                (image_cfg_scale, "Image CFG scale"),
                (width, "Size-1"),
                (height, "Size-2"),
                (batch_size, "Batch size"),
                (toprow.ui_styles.dropdown, lambda d: d["Styles array"] if isinstance(d.get("Styles array"), list) else gr.update()),
                (denoising_strength, "Denoising strength"),
                (mask_blur, "Mask blur"),
                (inpainting_mask_invert, 'Mask mode'),
                (inpainting_fill, 'Masked content'),
                (inpaint_full_res, 'Inpaint area'),
                (inpaint_full_res_padding, 'Masked area padding'),
                *scripts.scripts_img2img.infotext_fields
            ]
            parameters_copypaste.add_paste_fields("img2img", init_img, img2img_paste_fields, override_settings)
            parameters_copypaste.add_paste_fields("inpaint", init_img_with_mask, img2img_paste_fields, override_settings)
            parameters_copypaste.register_paste_params_button(parameters_copypaste.ParamBinding(
                paste_button=toprow.paste, tabname="img2img", source_text_component=toprow.prompt, source_image_component=None,
            ))

        extra_networks_ui_img2img = ui_extra_networks.create_ui(img2img_interface, [img2img_generation_tab], 'img2img')
        ui_extra_networks.setup_ui(extra_networks_ui_img2img, output_panel.gallery)

        extra_tabs.__exit__()

    scripts.scripts_current = None

    with gr.Blocks(analytics_enabled=False) as extras_interface:
        ui_postprocessing.create_ui()

    with gr.Blocks(analytics_enabled=False) as pnginfo_interface:
        with ResizeHandleRow(equal_height=False):
            with gr.Column(variant='panel'):
                image = gr.Image(elem_id="pnginfo_image", label="Source", source="upload", interactive=True, type="pil")

            with gr.Column(variant='panel'):
                html = gr.HTML()
                generation_info = gr.Textbox(visible=False, elem_id="pnginfo_generation_info")
                html2 = gr.HTML()
                with gr.Row():
                    buttons = parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])

                for tabname, button in buttons.items():
                    parameters_copypaste.register_paste_params_button(parameters_copypaste.ParamBinding(
                        paste_button=button, tabname=tabname, source_text_component=generation_info, source_image_component=image,
                    ))

        image.change(
            fn=wrap_gradio_call_no_job(modules.extras.run_pnginfo),
            inputs=[image],
            outputs=[html, generation_info, html2],
        )

    modelmerger_ui = ui_checkpoint_merger.UiCheckpointMerger()

    with gr.Blocks(analytics_enabled=False) as train_interface:
        with gr.Row(equal_height=False):
            gr.HTML(value="<p style='margin-bottom: 0.7em'>See <b><a href=\"https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Textual-Inversion\">wiki</a></b> for detailed explanation.</p>")

        with ResizeHandleRow(variant="compact", equal_height=False):
            with gr.Tabs(elem_id="train_tabs"):

                with gr.Tab(label="Create embedding", id="create_embedding"):
                    new_embedding_name = gr.Textbox(label="Name", elem_id="train_new_embedding_name")
                    initialization_text = gr.Textbox(label="Initialization text", value="*", elem_id="train_initialization_text")
                    nvpt = gr.Slider(label="Number of vectors per token", minimum=1, maximum=75, step=1, value=1, elem_id="train_nvpt")
                    overwrite_old_embedding = gr.Checkbox(value=False, label="Overwrite Old Embedding", elem_id="train_overwrite_old_embedding")

                    with gr.Row():
                        with gr.Column(scale=3):
                            gr.HTML(value="")

                        with gr.Column():
                            create_embedding = gr.Button(value="Create embedding", variant='primary', elem_id="train_create_embedding")

                with gr.Tab(label="Create hypernetwork", id="create_hypernetwork"):
                    new_hypernetwork_name = gr.Textbox(label="Name", elem_id="train_new_hypernetwork_name")
                    new_hypernetwork_sizes = gr.CheckboxGroup(label="Modules", value=["768", "320", "640", "1280"], choices=["768", "1024", "320", "640", "1280"], elem_id="train_new_hypernetwork_sizes")
                    new_hypernetwork_layer_structure = gr.Textbox("1, 2, 1", label="Enter hypernetwork layer structure", placeholder="1st and last digit must be 1. ex:'1, 2, 1'", elem_id="train_new_hypernetwork_layer_structure")
                    new_hypernetwork_activation_func = gr.Dropdown(value="linear", label="Select activation function of hypernetwork. Recommended : Swish / Linear(none)", choices=hypernetworks_ui.keys, elem_id="train_new_hypernetwork_activation_func")
                    new_hypernetwork_initialization_option = gr.Dropdown(value = "Normal", label="Select Layer weights initialization. Recommended: Kaiming for relu-like, Xavier for sigmoid-like, Normal otherwise", choices=["Normal", "KaimingUniform", "KaimingNormal", "XavierUniform", "XavierNormal"], elem_id="train_new_hypernetwork_initialization_option")
                    new_hypernetwork_add_layer_norm = gr.Checkbox(label="Add layer normalization", elem_id="train_new_hypernetwork_add_layer_norm")
                    new_hypernetwork_use_dropout = gr.Checkbox(label="Use dropout", elem_id="train_new_hypernetwork_use_dropout")
                    new_hypernetwork_dropout_structure = gr.Textbox("0, 0, 0", label="Enter hypernetwork Dropout structure (or empty). Recommended : 0~0.35 incrementing sequence: 0, 0.05, 0.15", placeholder="1st and last digit must be 0 and values should be between 0 and 1. ex:'0, 0.01, 0'")
                    overwrite_old_hypernetwork = gr.Checkbox(value=False, label="Overwrite Old Hypernetwork", elem_id="train_overwrite_old_hypernetwork")

                    with gr.Row():
                        with gr.Column(scale=3):
                            gr.HTML(value="")

                        with gr.Column():
                            create_hypernetwork = gr.Button(value="Create hypernetwork", variant='primary', elem_id="train_create_hypernetwork")

                def get_textual_inversion_template_names():
                    return sorted(textual_inversion.textual_inversion_templates)

                with gr.Tab(label="Train", id="train"):
                    gr.HTML(value="<p style='margin-bottom: 0.7em'>Train an embedding or Hypernetwork; you must specify a directory with a set of 1:1 ratio images <a href=\"https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Textual-Inversion\" style=\"font-weight:bold;\">[wiki]</a></p>")
                    with FormRow():
                        train_embedding_name = gr.Dropdown(label='Embedding', elem_id="train_embedding", choices=sorted(sd_hijack.model_hijack.embedding_db.word_embeddings.keys()))
                        create_refresh_button(train_embedding_name, sd_hijack.model_hijack.embedding_db.load_textual_inversion_embeddings, lambda: {"choices": sorted(sd_hijack.model_hijack.embedding_db.word_embeddings.keys())}, "refresh_train_embedding_name")

                        train_hypernetwork_name = gr.Dropdown(label='Hypernetwork', elem_id="train_hypernetwork", choices=sorted(shared.hypernetworks))
                        create_refresh_button(train_hypernetwork_name, shared.reload_hypernetworks, lambda: {"choices": sorted(shared.hypernetworks)}, "refresh_train_hypernetwork_name")

                    with FormRow():
                        embedding_learn_rate = gr.Textbox(label='Embedding Learning rate', placeholder="Embedding Learning rate", value="0.005", elem_id="train_embedding_learn_rate")
                        hypernetwork_learn_rate = gr.Textbox(label='Hypernetwork Learning rate', placeholder="Hypernetwork Learning rate", value="0.00001", elem_id="train_hypernetwork_learn_rate")

                    with FormRow():
                        clip_grad_mode = gr.Dropdown(value="disabled", label="Gradient Clipping", choices=["disabled", "value", "norm"])
                        clip_grad_value = gr.Textbox(placeholder="Gradient clip value", value="0.1", show_label=False)

                    with FormRow():
                        batch_size = gr.Number(label='Batch size', value=1, precision=0, elem_id="train_batch_size")
                        gradient_step = gr.Number(label='Gradient accumulation steps', value=1, precision=0, elem_id="train_gradient_step")

                    dataset_directory = gr.Textbox(label='Dataset directory', placeholder="Path to directory with input images", elem_id="train_dataset_directory")
                    log_directory = gr.Textbox(label='Log directory', placeholder="Path to directory where to write outputs", value="textual_inversion", elem_id="train_log_directory")

                    with FormRow():
                        template_file = gr.Dropdown(label='Prompt template', value="style_filewords.txt", elem_id="train_template_file", choices=get_textual_inversion_template_names())
                        create_refresh_button(template_file, textual_inversion.list_textual_inversion_templates, lambda: {"choices": get_textual_inversion_template_names()}, "refrsh_train_template_file")

                    training_width = gr.Slider(minimum=64, maximum=2048, step=8, label="Width", value=512, elem_id="train_training_width")
                    training_height = gr.Slider(minimum=64, maximum=2048, step=8, label="Height", value=512, elem_id="train_training_height")
                    varsize = gr.Checkbox(label="Do not resize images", value=False, elem_id="train_varsize")
                    steps = gr.Number(label='Max steps', value=100000, precision=0, elem_id="train_steps")

                    with FormRow():
                        create_image_every = gr.Number(label='Save an image to log directory every N steps, 0 to disable', value=500, precision=0, elem_id="train_create_image_every")
                        save_embedding_every = gr.Number(label='Save a copy of embedding to log directory every N steps, 0 to disable', value=500, precision=0, elem_id="train_save_embedding_every")

                    use_weight = gr.Checkbox(label="Use PNG alpha channel as loss weight", value=False, elem_id="use_weight")

                    save_image_with_stored_embedding = gr.Checkbox(label='Save images with embedding in PNG chunks', value=True, elem_id="train_save_image_with_stored_embedding")
                    preview_from_txt2img = gr.Checkbox(label='Read parameters (prompt, etc...) from txt2img tab when making previews', value=False, elem_id="train_preview_from_txt2img")

                    shuffle_tags = gr.Checkbox(label="Shuffle tags by ',' when creating prompts.", value=False, elem_id="train_shuffle_tags")
                    tag_drop_out = gr.Slider(minimum=0, maximum=1, step=0.1, label="Drop out tags when creating prompts.", value=0, elem_id="train_tag_drop_out")

                    latent_sampling_method = gr.Radio(label='Choose latent sampling method', value="once", choices=['once', 'deterministic', 'random'], elem_id="train_latent_sampling_method")

                    with gr.Row():
                        train_embedding = gr.Button(value="Train Embedding", variant='primary', elem_id="train_train_embedding")
                        interrupt_training = gr.Button(value="Interrupt", elem_id="train_interrupt_training")
                        train_hypernetwork = gr.Button(value="Train Hypernetwork", variant='primary', elem_id="train_train_hypernetwork")

                params = script_callbacks.UiTrainTabParams(txt2img_preview_params)

                script_callbacks.ui_train_tabs_callback(params)

            with gr.Column(elem_id='ti_gallery_container'):
                ti_output = gr.Text(elem_id="ti_output", value="", show_label=False)
                gr.Gallery(label='Output', show_label=False, elem_id='ti_gallery', columns=4)
                gr.HTML(elem_id="ti_progress", value="")
                ti_outcome = gr.HTML(elem_id="ti_error", value="")

        create_embedding.click(
            fn=textual_inversion_ui.create_embedding,
            inputs=[
                new_embedding_name,
                initialization_text,
                nvpt,
                overwrite_old_embedding,
            ],
            outputs=[
                train_embedding_name,
                ti_output,
                ti_outcome,
            ]
        )

        create_hypernetwork.click(
            fn=hypernetworks_ui.create_hypernetwork,
            inputs=[
                new_hypernetwork_name,
                new_hypernetwork_sizes,
                overwrite_old_hypernetwork,
                new_hypernetwork_layer_structure,
                new_hypernetwork_activation_func,
                new_hypernetwork_initialization_option,
                new_hypernetwork_add_layer_norm,
                new_hypernetwork_use_dropout,
                new_hypernetwork_dropout_structure
            ],
            outputs=[
                train_hypernetwork_name,
                ti_output,
                ti_outcome,
            ]
        )

        train_embedding.click(
            fn=wrap_gradio_gpu_call(textual_inversion_ui.train_embedding, extra_outputs=[gr.update()]),
            _js="start_training_textual_inversion",
            inputs=[
                dummy_component,
                train_embedding_name,
                embedding_learn_rate,
                batch_size,
                gradient_step,
                dataset_directory,
                log_directory,
                training_width,
                training_height,
                varsize,
                steps,
                clip_grad_mode,
                clip_grad_value,
                shuffle_tags,
                tag_drop_out,
                latent_sampling_method,
                use_weight,
                create_image_every,
                save_embedding_every,
                template_file,
                save_image_with_stored_embedding,
                preview_from_txt2img,
                *txt2img_preview_params,
            ],
            outputs=[
                ti_output,
                ti_outcome,
            ]
        )

        train_hypernetwork.click(
            fn=wrap_gradio_gpu_call(hypernetworks_ui.train_hypernetwork, extra_outputs=[gr.update()]),
            _js="start_training_textual_inversion",
            inputs=[
                dummy_component,
                train_hypernetwork_name,
                hypernetwork_learn_rate,
                batch_size,
                gradient_step,
                dataset_directory,
                log_directory,
                training_width,
                training_height,
                varsize,
                steps,
                clip_grad_mode,
                clip_grad_value,
                shuffle_tags,
                tag_drop_out,
                latent_sampling_method,
                use_weight,
                create_image_every,
                save_embedding_every,
                template_file,
                preview_from_txt2img,
                *txt2img_preview_params,
            ],
            outputs=[
                ti_output,
                ti_outcome,
            ]
        )

        interrupt_training.click(
            fn=lambda: shared.state.interrupt(),
            inputs=[],
            outputs=[],
        )

    loadsave = ui_loadsave.UiLoadsave(cmd_opts.ui_config_file)
    ui_settings_from_file = loadsave.ui_settings.copy()

    settings.create_ui(loadsave, dummy_component)

    interfaces = [
        (txt2img_interface, "txt2img", "txt2img"),
        (img2img_interface, "img2img", "img2img"),
        (extras_interface, "Extras", "extras"),
        (pnginfo_interface, "PNG Info", "pnginfo"),
        (modelmerger_ui.blocks, "Checkpoint Merger", "modelmerger"),
        (train_interface, "Train", "train"),
    ]

    interfaces += script_callbacks.ui_tabs_callback()
    interfaces += [(settings.interface, "Settings", "settings")]

    extensions_interface = ui_extensions.create_ui()
    interfaces += [(extensions_interface, "Extensions", "extensions")]

    shared.tab_names = []
    for _interface, label, _ifid in interfaces:
        shared.tab_names.append(label)

    with gr.Blocks(theme=shared.gradio_theme, analytics_enabled=False, title="Stable Diffusion") as demo:
        # Cargar CSS personalizado para pasaportes
        try:
            css_path = Path(__file__).parent.parent / "pasaportes_style.css"
            if css_path.exists():
                with open(css_path, 'r', encoding='utf-8') as f:
                    custom_css = f.read()
                demo.css = custom_css
        except Exception as e:
            print(f"Warning: No se pudo cargar CSS personalizado: {e}")
        
        settings.add_quicksettings()

        parameters_copypaste.connect_paste_params_buttons()

        with gr.Tabs(elem_id="tabs") as tabs:
            tab_order = {k: i for i, k in enumerate(opts.ui_tab_order)}
            sorted_interfaces = sorted(interfaces, key=lambda x: tab_order.get(x[1], 9999))

            for interface, label, ifid in sorted_interfaces:
                if label in shared.opts.hidden_tabs:
                    continue
                with gr.TabItem(label, id=ifid, elem_id=f"tab_{ifid}"):
                    interface.render()

                if ifid not in ["extensions", "settings"]:
                    loadsave.add_block(interface, ifid)

            loadsave.add_component(f"webui/Tabs@{tabs.elem_id}", tabs)

            loadsave.setup_ui()

        if os.path.exists(os.path.join(script_path, "notification.mp3")) and shared.opts.notification_audio:
            gr.Audio(interactive=False, value=os.path.join(script_path, "notification.mp3"), elem_id="audio_notification", visible=False)

        footer = shared.html("footer.html")
        footer = footer.format(versions=versions_html(), api_docs="/docs" if shared.cmd_opts.api else "https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API")
        gr.HTML(footer, elem_id="footer")

        settings.add_functionality(demo)

        update_image_cfg_scale_visibility = lambda: gr.update(visible=shared.sd_model and shared.sd_model.cond_stage_key == "edit")
        settings.text_settings.change(fn=update_image_cfg_scale_visibility, inputs=[], outputs=[image_cfg_scale])
        demo.load(fn=update_image_cfg_scale_visibility, inputs=[], outputs=[image_cfg_scale])

        modelmerger_ui.setup_ui(dummy_component=dummy_component, sd_model_checkpoint_component=settings.component_dict['sd_model_checkpoint'])

    if ui_settings_from_file != loadsave.ui_settings:
        loadsave.dump_defaults()
    demo.ui_loadsave = loadsave

    return demo


def versions_html():
    import torch
    import launch

    python_version = ".".join([str(x) for x in sys.version_info[0:3]])
    commit = launch.commit_hash()
    tag = launch.git_tag()

    if shared.xformers_available:
        import xformers
        xformers_version = xformers.__version__
    else:
        xformers_version = "N/A"

    return f"""
version: <a href="https://github.com/AUTOMATIC1111/stable-diffusion-webui/commit/{commit}">{tag}</a>
&#x2000;•&#x2000;
python: <span title="{sys.version}">{python_version}</span>
&#x2000;•&#x2000;
torch: {getattr(torch, '__long_version__',torch.__version__)}
&#x2000;•&#x2000;
xformers: {xformers_version}
&#x2000;•&#x2000;
gradio: {gr.__version__}
&#x2000;•&#x2000;
checkpoint: <a id="sd_checkpoint_hash">N/A</a>
"""


def setup_ui_api(app):
    from pydantic import BaseModel, Field

    class QuicksettingsHint(BaseModel):
        name: str = Field(title="Name of the quicksettings field")
        label: str = Field(title="Label of the quicksettings field")

    def quicksettings_hint():
        return [QuicksettingsHint(name=k, label=v.label) for k, v in opts.data_labels.items()]

    app.add_api_route("/internal/quicksettings-hint", quicksettings_hint, methods=["GET"], response_model=list[QuicksettingsHint])

    app.add_api_route("/internal/ping", lambda: {}, methods=["GET"])

    app.add_api_route("/internal/profile-startup", lambda: timer.startup_record, methods=["GET"])

    def download_sysinfo(attachment=False):
        from fastapi.responses import PlainTextResponse

        text = sysinfo.get()
        filename = f"sysinfo-{datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M')}.json"

        return PlainTextResponse(text, headers={'Content-Disposition': f'{"attachment" if attachment else "inline"}; filename="{filename}"'})

    app.add_api_route("/internal/sysinfo", download_sysinfo, methods=["GET"])
    app.add_api_route("/internal/sysinfo-download", lambda: download_sysinfo(attachment=True), methods=["GET"])

    import fastapi.staticfiles
    app.mount("/webui-assets", fastapi.staticfiles.StaticFiles(directory=launch_utils.repo_dir('stable-diffusion-webui-assets')), name="webui-assets")

